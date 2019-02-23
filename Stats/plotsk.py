#time evaluation CBFREQ
import pandas as pd
import pickle
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import hdbscan
import matplotlib.pyplot as plt
import numpy as np
import math
import SkAlgs as sky
import time
def Sub_Analysis(categs, clusters, k):
    array_name = 'procdata.txt'
    with open(array_name, 'rb') as fileread:
        # read the data as binary data stream
        array = pickle.load(fileread)
        # print("Dataset size: ", len(array))
        # print("Number of dimensions: ", len(array[0]))
        # print(array)

    counter = 1
    retids = []
    for key, value in categs.items():
        # print("Cluster ", key, "Size ",len(value))
        # printCluster(value)
        n = math.ceil(k / nclusters)
        # print("To be choosen:",n)
        dat = [array[i] for i in value]
        # print(dat)
        counter = counter + 1

        R = sky.TopkFreqSK(dat, 3, n)
        # print("R = ",R)
        freqids = [i[0] for i in R]
        # print(freqids)
        # print("returned ids")
        for fitem in freqids:
            # print(value[fitem])
            retids.append(value[fitem])
    # print("Items to be returned:",retids,", length =",len(retids))
    return retids




global df
df = pd.read_csv("processeddf.csv", encoding="ISO-8859-1", na_values="")

df = df.drop('vehicleType', axis=1)
df = df.drop('fuelType', axis=1)
df = df.drop('notRepairedDamage', axis=1)
df = df.drop('gearbox', axis=1)
print(list(df))

dataset = df.as_matrix()
print("Dataset size=", len(dataset))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

n = 100
c = 'b'
ma = 'o'

ax.scatter(dataset[:,0], dataset[:,1], dataset[:,2], c=c, marker=ma)

ax.set_xlabel('Price')
ax.set_ylabel('Horsepower')
ax.set_zlabel('Mileage')
ax.set_title('Dataset')
plt.show()



# open ids of reduced sets
skids = pickle.load(open('SKcars.txt', 'rb'))
print("Skyline size=", len(skids))
dfsk = df.iloc[skids]

msk = dfsk.as_matrix()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

n = 100
c = 'b'
ma = 'o'

print("M0-,",msk[0,0])
ax.scatter(msk[:,0], msk[:,1], msk[:,2], c=c, marker=ma)

ax.set_xlabel('Price')
ax.set_ylabel('Horsepower')
ax.set_zlabel('Mileage')
ax.set_title('Skyline set')
plt.show()


#### DBR SKYLINE ########
k=15
start_dbr=time.time()
idsdbr = sky.DBR(skids,k)#pickle.load(open('DBRIds.txt', 'rb'))
end_dbr = time.time()
print("Time for dbr:", round(end_dbr-start_dbr, 3))
print("IDS dbr len=", len(idsdbr))
dfdbr = df.iloc[idsdbr]
mdbr = dfdbr.as_matrix()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

n = 100
c = 'b'
ma = 'o'

ax.scatter(mdbr[:,0], mdbr[:,1], mdbr[:,2], c=c, marker=ma)

ax.set_xlabel('Price')
ax.set_ylabel('Horsepower')
ax.set_zlabel('Mileage')
ax.set_title('DBR set k=%s'%k)
plt.show()

#############################

estimators = [ ('hdbscan 10', hdbscan.HDBSCAN(min_cluster_size=k, gen_min_span_tree=True)),
                ('k_means_10', KMeans(n_clusters=k)),
              ('k_means_8', KMeans(n_clusters=8)),
              ('k_means_6', KMeans(n_clusters=6)),
              ('k_means_4', KMeans(n_clusters=4)),
              ('hdbscan 10', hdbscan.HDBSCAN(min_cluster_size=16, gen_min_span_tree=True)),
              ('hdbscan 8', hdbscan.HDBSCAN(min_cluster_size=12, gen_min_span_tree=True)),
                ('hdbscab 6', hdbscan.HDBSCAN(min_cluster_size=8, gen_min_span_tree=True)),
                ('hdbscab 4', hdbscan.HDBSCAN(min_cluster_size=4, gen_min_span_tree=True)),
              ]


fignum = 0
titles = ['HDBSCAN '+str(k)+' minpts', 'k-Means 8 clusters', 'k-Means 6 clusters', 'k-Means 4 clusters', 'Hdbscan 16 Minpts ', 'Hdbscan 12 Minpts', 'Hdbscan 8 Minpts', 'Hdbscan 4 Minpts']
for name, est in estimators:
    start_time = time.time()
    est.fit(msk)
    labels = est.labels_

    clusterids = set(labels)
    nclusters = len(clusterids)
    print("N clusters=", nclusters)
    categs = {}
    for id in clusterids:
        indices = [i for i, x in enumerate(labels) if x == id]
        categs[id] = [skids[indice] for indice in indices]

    print(categs)

    redids = Sub_Analysis(categs, nclusters, nclusters)
    end_time = time.time()
    print("k means",k," took:", round(end_time-start_time,2))
    print("Reduced size=", len(redids))
    print("redids=",redids)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    n = 100
    c = 'b'
    ma = 'o'

    dfred = df.iloc[redids]
    mred = dfred.as_matrix()

    ax.scatter(mred[:, 0], mred[:, 1], mred[:, 2], c=c, marker=ma)

    ax.set_xlabel('Price')
    ax.set_ylabel('Horsepower')
    ax.set_zlabel('Mileage')
    ax.set_title('Reduced set '+titles[fignum])



    fig = plt.figure(fignum, figsize=(4, 3))
    ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
    ax.scatter(msk[:, 0], msk[:, 1], msk[:, 2],
               c=labels.astype(np.float), edgecolor='k')

    # ax.w_xaxis.set_ticklabels([])
    # ax.w_yaxis.set_ticklabels([])
    # ax.w_zaxis.set_ticklabels([])
    ax.set_xlabel('Price')
    ax.set_ylabel('Horsepower')
    ax.set_zlabel('Mileage')
    ax.set_title(titles[fignum])
    ax.dist = 12

    plt.show()
    fignum = fignum + 1
plt.show()


