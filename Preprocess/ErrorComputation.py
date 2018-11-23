
import numpy as np
from scipy.spatial import distance

#fuction to compute sampling error
def samplingerror(array, skids, *argv ):

    errors = []
    skset = [array[id] for id in skids]
    skmeans = getmeans(skset)

    for arg in argv:
        set = [array[id] for id in arg]
        setmeans = getmeans(set)

        error = distance.euclidean(skmeans, setmeans)
        errors.append(round(error, 2))

    print("Sampling Error")
    print("k-Dominant: ", errors[0])
    print("Skyline frequency: ", errors[1])
    print("Random Reduction: ", errors[2])
    print("Distance Based Representatives: ", errors[3])
    print("Density Based frequency: ", errors[4])

    results = {}
    results['type'] = "sampling error"
    results['kdom'] = errors[0]
    results['skfreq'] = errors[1]
    results['random'] = errors[2]
    results['dbr'] = errors[3]
    results['dbfreq'] = errors[4]
    return results

#function to get means of numerical data
def getmeans(array):

    if not array:
        return [0,0,0]

    price = [row[0] for row in array]
    hp = [row[1] for row in array]
    mileage = [row[2] for row in array]

    means = [round(np.mean(price),2), round(np.mean(hp),2), round(np.mean(mileage),2)]

    return means

#function to compute the sumarization error
def SumError(array, skids, *argv ):

    skset = [array[id] for id in skids]
    skmeans = binmeans(skset)
    skmeans = [item for sublist in skmeans for item in sublist]

    distlist = []
    for arg in argv:
        set = [array[id] for id in arg]
        setmeans = binmeans(set)
        setmeans = [item for sublist in setmeans for item in sublist]

        dist = round(distance.euclidean(setmeans, skmeans), 2)
        distlist.append(dist)

    print("Summarization Error:")
    print("k-Dominant: ", distlist[0])
    print("Skyline frequency: ", distlist[1])
    print("Random Reduction: ", distlist[2])
    print("Distance Based Representatives: ", distlist[3])
    print("Density Based frequency: ", distlist[4])

    results = {}
    results['type'] = "summarization error"
    results['kdom'] = distlist[0]
    results['skfreq'] = distlist[1]
    results['random'] = distlist[2]
    results['dbr'] = distlist[3]
    results['dbfreq'] = distlist[4]

    return results

def binmeans(array):
    #returns a vector of the means for each attribute according to price bins
    means = []
    for d in range(1,6):
        bin = [x for x in array if x[0]==d]
        means.append(getmeans(bin) )

    for d in range(1,6):
        bin = [x for x in array if x[1]==d]
        means.append(getmeans(bin))

    for d in range(1,4):
        bin = [x for x in array if x[2]==d]
        means.append(getmeans(bin))

    return means
