import numpy as np
import SkAlgs as sky
from sklearn.cluster import KMeans
import math
import time
import hdbscan

def Sub_Analysis(ls, categs, clusters, k, d ):


    counter = 1
    retids = []
    for key, value in categs.items():
        # print("Cluster ", key, "Size ",len(value))
        # printCluster(value)
        print("value=", value)
        n = math.ceil(k / nclusters)
        # print("To be choosen:",n)

        dat = [ls[i] for i in value]
        # print(dat)
        counter = counter + 1

        R = sky.TopkFreqSK(dat, d, n)
        # print("R = ",R)
        freqids = [i[0] for i in R]
        # print(freqids)
        # print("returned ids")
        for fitem in freqids:
            # print(value[fitem])
            retids.append(value[fitem])
    # print("Items to be returned:",retids,", length =",len(retids))
    return retids

N=1000
d=5
p=5
times = []
#for d in range(5,16):
print("d=",d,",p=",p)
ar = np.random.rand(N, d)
ls=[]
pivot = 1/N
for i in range(0,N):

    ar[i,0]= round(0+pivot,4)
    ar[i,1] = round(1-pivot,4)

    pivot = pivot+1/N

    #ids = sky.BNL(ls,2)
    #print("len=",len(ids))
import matplotlib.pyplot as plt
print(ar)
datlist = ar.tolist()
plt.plot(ar[:,0], ar[:,1], 'ro')
plt.show()


est = [KMeans(n_clusters=p), hdbscan.HDBSCAN(min_cluster_size=p, gen_min_span_tree=True) ]
alg = est[1]
start = time.time()
#alg = KMeans(n_clusters=15)
alg.fit(ar)
#y_pred = alg.predict(ar)
end = time.time()
cluster_time=end-start

labels = alg.labels_
clusterids = set(labels)
nclusters = len(clusterids)

categs = {}

for id in clusterids:

    indices = [i for i, x in enumerate(labels) if x == id]

    categs[id] = indices#[datlist[indice] for indice in indices]

start = time.time()
ret = Sub_Analysis(datlist, categs, nclusters, 1, d)
end = time.time()
sub_time = end-start
print("total time in sec", sub_time+cluster_time)

time=sub_time+cluster_time

print("total time=",time)
