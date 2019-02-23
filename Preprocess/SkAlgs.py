
import numbers
import numpy as np
import operator
import random
import pickle
import math
import pandas as pd
import hdbscan

def BNL(ls, N):
    #input parameters
    #ls: a list with the objects,
    #N: the number of dimensions

    #output
    #window: a list containing the ids of the skyline objects

    #window for comparing
    window = []

    #place the first id in the window
    window.append(0)

    for idx in range(1, len(ls)):
        dom = False
        #compare each object with the window
        for witem in window:
            if comp_k(ls[witem], ls[idx], N, N):
                #object is dominated by the window
                dom = True

        if dom == False:
            #append object to window
            window.append(idx)

            #delete all the objects in the window dominated by element
            window = [x for x in window if not comp_k(ls[idx], ls[x], len(ls[1]), N)]

    return window

def count(ls):
    #takes a list of 'LS', 'GR', 'EQ'
    #and returns a dictionary with the values
    ctEQ = ctGR = ctLS = 0
    for item in ls:
        if item == 'LS':
            ctLS = ctLS+1
        elif item == 'GR':
            ctGR = ctGR+1
        elif item == 'EQ':
            ctEQ = ctEQ+1
    dict = {'LS':ctLS, 'GR':ctGR, 'EQ':ctEQ}
    return dict

def compare(a,b):
    #compares a and b and returns 'GR','LS','EQ'
    if isinstance(a, numbers.Number):
        if a>b:
            return 'GR'
        elif a<b:
            return 'LS'
        else:
            return 'EQ'
    else:
        if (a[0]==b[0] and a[1] == b[1]):
            return 'EQ'
        elif (b[0]>=a[0] and b[1]<= a[1]):
            return 'GR'
        elif (a[0] >= b[0] and a[1] <= b[1]):
            return 'LS'
        else:
            return 'INC'

def comp_k(a, b, K, N):
    #returns True if a k-dominates b
    #returns False otherwise
    res=[]
    for aitem, bitem in zip(a, b):
        res.append(compare(aitem,bitem))
        dict = count(res)

    if (K==N):
        if dict['EQ']==N:
            return False
        if 'INC' in res:
            return False
        c = dict['GR']+dict['EQ']
        if c==N:
            return True
        return False

    if dict['GR']>=1 and dict['EQ']>=K-dict['GR']:
        return True
    return False

def TwoScan(D, N, k):

    R = []
    for p in range (0, len(D)):
        isDom = True
        for pbar in R:
            if comp_k(D[pbar], D[p], k, N):
                isDom = False
            if comp_k(D[p], D[pbar], k, N):
                #R.remove(pbar)
                R = [x for x in R if D[x]!=D[pbar] ]
        if (isDom):
            R.append(p)

    for p in range(0, len(D)):
        for pbar in R:
            if p!=pbar:
                if comp_k(D[p],D[pbar],k,N):
                    #R.remove(pbar)
                    R = [ x for x in R if D[x] != D[pbar] ]

    return R

def kDominance(D, N, delta):
    kmin = 1
    kmax = N
    R = []
    while(True):
        k = int((kmin+kmax)/2)
        T = TwoScan(D, N, k)
        if len(T)== delta:
            R = T
            kmin = kmax + 1
        elif len(T)>delta:
            R = T
            kmin = k+1
        else:
            kmax = k-1
        if kmin>kmax:
            break
    return R

def ChooseRandom(N):
    with open('SKcars.txt', 'rb') as fileread:
        # read the data as binary data stream
        skl = pickle.load(fileread)
    #skdf = df.iloc[skl, :]
    itemsid = random.sample(skl, int(N))
    return itemsid


#### Code for ranking
def Union(lst1, lst2):
    final_list = list(set(lst1) | set(lst2))
    return final_list

def Covers(DSa, DSb):
    #returns True if DSa covers DSb, both are of the form (U, V)
    flag1 = set(DSb[0]).issubset(set(DSa[0]))
    flag2 = set(DSb[1]).issubset(set(DSa[1]))
    return flag1 and flag2

def ApproxCountDomSub(M, eps, delta):

    N = []
    M = list(M)

    for m in M:
        # m = (U, V), U = m[0], V = m[1]

        ni = (pow(2, len(m[0]))-1)*(pow(2, len(m[1])))
        N.append(ni)
    sumN = sum(N)
    T = (2*len(M)*np.log(2/delta))/pow(eps,2)
    #print("N=",sumN,",T=",T)
    C = 0
    for i in range(1, int(T+1)):
        #ch = random
        Mi = random.sample(range(0, len(M)), 1)
        m = M[Mi[0]]

        nleft = 0
        nright = 0
        if len(m[0])!=0:
            nleft = random.sample(range(1, len(m[0])+1), 1)
            nleft = nleft[0]
        if len(m[1])!=0:
            nright = random.sample(range(1, len(m[1])+1), 1)
            nright = nright[0]
        #print("nleft=", nleft, ",nright=",nright)


        chleft = random.sample(m[0], nleft)
        chright = random.sample(m[1], nright)
        #print("chleft = ",chleft,",chright=",chright)
        UV = [chleft,chright]
        #print("UV = ", UV)
        flag = False
        for j in range(0,Mi[0]):
            #if UV not covered by Mj
            if Covers(M[j], UV):
                flag = True
        if flag==False:
            C = C+1
        #print("C=",C)
    ret = sumN*(C/T)
    #print("returned = ", ret)
    return ret

def computeUV(a,b):
    #counting of dimensions start from 0
    U = []
    V = []
    # else:
    for d in range(0,len(a)):
        if isinstance(a[d], numbers.Number):
            if a[d] > b[d]:
                U.append(d)
            elif a[d] == b[d]:
                V.append(d)
        else:

            if (a[d][0] == b[d][0] and a[d][1] == b[d][1]):
                V.append(d)
            elif (b[d][0] >= a[d][0] and b[d][1] <= a[d][1]):
                U.append(d)
            elif (a[d][0] >= b[d][0] and a[d][1] <= b[d][1]):
                pass
            else:
                V.append(d)

    t = [U, V]
    return t


def TopkFreqSK(D, S, k):
    theta = pow(2,S)-1
    R = []

    eps = 0.1
    delta = 1
    for idx, p in enumerate(D,0):
        M = ComputeMaxSubspaceSets(D, S, p, k, theta, len(R))

        dp = ApproxCountDomSub(M, eps, delta)
        t = (idx, dp)
        if (len(R)<k) or (dp<theta):
            #remove()
            if len(R)==k:
                ma = max(R, key=operator.itemgetter(1))[1]
                R = [i for i in R if i[1] != ma]

            R.append(t)
            theta = max(R, key=operator.itemgetter(1))[1]

    return R

def ComputeMaxSubspaceSets(D, S, p, k, theta, r):
    M = []
    for q in D:
        if q!=p:
            #t = [U, V]
            t = computeUV(q,p)

            if (r==k) and (pow (2,len(t[0]))-1) *( pow(2, len(t[1])) ) >= theta:
                M.append(t)
                return M
            isMaximal = True
            for ss in M:
                #ss=(P,Q)
                UV = Union(t[0],t[1])
                PQ = Union(ss[0], ss[1])
                if (set(UV).issubset(set(PQ))) and (set(t[0]).issubset(set(ss[0]))):
                    isMaximal = False
                    break
                elif set(PQ).issubset(set(UV)) and set(ss[0]).issubset(set(t[0])):
                    M.remove(ss)
            if isMaximal:
                M.append(t)

    return M


###### ADR ##############3
def eucldist(a, b):
    #input two lists [1, 3.4, 5 ...] [2, 8, 0.1 ...]
    #returns the eucl distance of 2 points
    sum = 0
    headers = ['price', 'powerPS', 'kilometer']
    for h in headers:
        dif = a[h]-b[h]
        pow2 = pow(dif,2)
        sum = sum + pow2

    return math.sqrt(sum)

def DBR(sk, k):
    #initialize K the representative set to contain the first skyline item

    dfn = pd.read_csv("processeddf.csv", encoding="ISO-8859-1", na_values="")
    K = []
    K.append(sk[0])

    #put all the other skyline items in a list
    S = [ id for id in sk[1:] ]

    for i in range(1, k):
        #initialize the max representative distance to 0
        maxrepdist = 0
        #print("Loop ",i)
        #for each skyline item compute its nearest representative
        for skitem in S:
            repdist = 200000
            for r in K:
                dist = eucldist(dfn.iloc[skitem], dfn.iloc[r])
                #print("Dist =",dist)
                if dist<repdist:
                    repdist = dist
                    minskitem = skitem
            #print("SKITEM:", skitem, "Min dist is from repres:", minidx ," dist=", repdist)
            #compute the maximun representative distance among all non represenative skyline points
            if repdist > maxrepdist:
                #print("Found Max")
                maxrepdist = repdist
                maxskitem = minskitem
            #print("idmax = ", maxskitem, "maxrepdist=",maxrepdist,"")
        K.append(maxskitem)
        S = [skit for skit in S if skit!=maxskitem]

    return list(set(K))

def dist(M, h):
    Dist = [[0 for x in range(h)] for y in range(h)]
    print("Distance function")
    print(h)
    for rindex in range(0, h):
        for oindex in range(rindex+1, h):
            d = round(eucldist(M[rindex], M[oindex]),2)

            Dist[rindex][oindex] = d
            Dist[oindex][rindex] = d

    return Dist

def DBSKFREQ(df, skids, k):
    #
    mask = df.iloc[skids]

    mask = mask.drop('vehicleType', axis=1)
    mask = mask.drop('gearbox', axis=1)
    mask = mask.drop('fuelType', axis=1)
    mask = mask.drop('notRepairedDamage', axis=1)

    #print(mask)


    clustererdf = hdbscan.HDBSCAN(min_cluster_size=4).fit(mask)


    #print(clustererdf.labels_)

    labels = list(clustererdf.labels_)


    clusterids = set(labels)
    nclusters = len(clusterids)

    categs = {}
    for id in clusterids:
        indices = [i for i, x in enumerate(labels) if x == id]
        categs[id] = [skids[indice] for indice in indices]
    #print(categs)

    array_name = 'procdata.txt'
    with open(array_name, 'rb') as fileread:
        # read the data as binary data stream
        array = pickle.load(fileread)
        #print("Dataset size: ", len(array))
        #print("Number of dimensions: ", len(array[0]))
        #print(array)

    counter = 1
    retids = []
    for key, value in categs.items():
        #print("Cluster ", key, "Size ",len(value))
        #printCluster(value)
        n = math.ceil(len(value)/2)
        #print("To be choosen:",n)
        dat = [array[i] for i in value]
        #print(dat)
        counter = counter + 1

        R = TopkFreqSK(dat, 7, n)
        #print("R = ",R)
        freqids = [i[0] for i in R]
        #print(freqids)
        #print("returned ids")
        for fitem in freqids:
            #print(value[fitem])
            retids.append(value[fitem])
    #print("Items to be returned:",retids,", length =",len(retids))
    return retids


def printCluster(ids):
    dataset_name = "processeddf.csv"
    global dfcl
    dfcl = pd.read_csv(dataset_name)

    #dfcl = dfcl.drop('vehicleType', axis=1)
    dfcl = dfcl.drop('gearbox', axis=1)
    #dfcl = dfcl.drop('fuelType', axis=1)
    #dfcl = dfcl.drop('notRepairedDamage', axis=1)

    dfcluster = dfcl.iloc[ids]
    #dfcabrio = dfcl[ (dfcl.powerPS>300) & (dfcl.vehicleType=='cabrio') & (dfcl.notRepairedDamage=='no')  ]

    print(dfcluster)

# D = [[1, 10, (3,4), (6,7)],[2,9,(2,3),(3,4)],[3,8,(1,2),(7,8)], [4,5,(3,4),(1,2)],[5,4,(2,3),(4,5)],
#     [6,3,(5,6),(7,8)], [7,2,(1,2),(2,3)], [10,1,(1,2)] , [1,10,(1,5),(6,7)],[2,9,(2,3),(3,4)]]
#
# sk = [0,1,2,3,4,5,6,7]
#
# k = 9
# ids = DBR(D,sk,k)
# print(len(ids))
ids = [1,23,56,76,43,89,10]
print(np.random.choice(ids, 3))
