import pandas as pd
import Preprocess as prec
import SkAlgs as sky
import pickle
import ErrorComputation as stat
import json

if __name__== "__main__":

    #read csv file and create dataframe
    dataset_name = "newcars.csv"
    dfcars = pd.read_csv(dataset_name, encoding="ISO-8859-1", na_values="")

    #preprocess dataframe
    processeddf = prec.CarsPreprocess(dfcars, 2000)

    print (processeddf.head())
    print (processeddf.tail())

    print ("New headers = ", list(processeddf))
    headers = list(processeddf)
    print(len(list(processeddf)))

    #transform dataframe to list of lists
    data = prec.df_to_array(processeddf)
    print(data)
    with open('procdata.txt', 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(data, filehandle)

    N = len(data[1])
    print("Number of attributes:", N)

    sk = sky.BNL(data, N)
    sk = list(set(sk))
    sk.sort()
    print ("SK autos = ", sk)

    #store skyline ids
    with open('SKcars.txt', 'wb') as filehandle:

        pickle.dump(sk, filehandle)

    print("BNL Skyline size = ", len(sk))
    datasize = len(data)
    perc = float(len(sk)) * 100 / datasize
    print("BNL SK Percentage of database  = ", round(perc, 2), '%')


    dfnew = pd.read_csv("processeddf.csv", encoding="ISO-8859-1", na_values="")
    print(list(dfnew))
    print(dfnew.head())

    #compute k-dominant skyline
    idsdom = sky.TwoScan(data, 7, 6)
    print("Ids k-Dominance = ", idsdom)
    print("k-Dominant size = ", len(idsdom))

    #compute dbr skyline
    k = int(len(sk)/2)
    DBRids = sky.DBR(sk, k)
    print("DBR size =", len(DBRids))

    #compute top-k frequent skyline set
    print("k=", k)
    R = sky.TopkFreqSK(data, 7, k)
    print("R =", R)
    freqids = [i[0] for i in R]
    print("SK freq size = ", len(freqids))

    #compute random skyline set
    randomids = sky.ChooseRandom(k)
    print("Random size = ", len(randomids))

    #compute density based skyline set
    myalg = sky.DBSKFREQ(processeddf, sk, k)
    print("DBSK size =", len(myalg))

    #compute sampling and summariation
    sampling_error = stat.samplingerror(data, sk, idsdom, freqids, randomids, DBRids, myalg)
    summ_error = stat.SumError(data, sk, idsdom, freqids, randomids, DBRids, myalg)

   #write all skyline sets to datafiles
    with open('SKcars.txt', 'wb') as filehandle:
        pickle.dump(sk, filehandle, protocol=2)

    with open('IdsDom.txt', 'wb') as filehandle:
        pickle.dump(idsdom, filehandle, protocol=2)

    with open('FreqIds.txt', 'wb') as filehandle:
        pickle.dump(freqids, filehandle, protocol=2)

    with open('RandomIds.txt', 'wb') as filehandle:
        pickle.dump(randomids, filehandle, protocol=2)

    with open('DBRIds.txt', 'wb') as filehandle:
        pickle.dump(DBRids, filehandle, protocol=2)

    with open('DBSK.txt', 'wb') as filehandle:
        pickle.dump(myalg, filehandle, protocol=2)

    with open('SamplingError.dat', 'w') as file:
        file.write(json.dumps(sampling_error))

    with open('SummError.dat', 'w') as file:
        file.write(json.dumps(summ_error))