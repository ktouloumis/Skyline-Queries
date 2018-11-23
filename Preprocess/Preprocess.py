import CategAttr as ca
import NumAttr as nm
import pandas as pd
import numpy as np

def CarsPreprocess(df, size):

    #drop unwanted columns for skyline dominance
    df = df.drop('dateCrawled', axis=1)
    df = df.drop('seller', axis=1)
    df = df.drop('offerType', axis=1)
    df = df.drop('abtest', axis=1)
    df = df.drop('yearOfRegistration', axis=1)
    df = df.drop('model', axis=1)
    df = df.drop('monthOfRegistration', axis=1)
    df = df.drop('dateCreated', axis=1)
    df = df.drop('nrOfPictures', axis=1)
    df = df.drop('postalCode', axis=1)
    df = df.drop('lastSeen', axis=1)
    df = df.drop('name', axis=1)
    df = df.drop('brand', axis=1)

    #drop null values
    df = df.dropna()

    df = df[df.price >= 5000 ]
    df = df[df.price<90000]
    df = df[df.powerPS < 500]
    df = df[df.powerPS > 50]

    #replace german words with english
    df = df.replace('nein','no')
    df = df.replace('ja', 'yes')
    df = df.replace('benzin', 'gas')
    df = df.replace('andere', 'other')
    df = df.replace('manuell', 'manual')
    df = df.replace('automatik', 'automatic')
    df = df.replace('kleinwagen', 'wagon')

    #sample dataframe
    print("Shape = ",df.shape)
    global samplesize
    samplesize = size
    dfsampled = df.sample(n=size)
    Statnalysis(df)
    dfsampled.to_csv("processeddf.csv", index = False)

    print(dfsampled.dtypes)
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']

    #select only numeric values
    numdf = dfsampled.select_dtypes(include=numerics)

    #process numerical attributes
    numdf = nm.NumPreprocess(numdf)

    #select categorical values
    categ_df = dfsampled.select_dtypes(include=['object']).copy()

    #process categorical data
    categ_df = ca.CategPrep.CategPreprocess(categ_df)

    #merge categorical and numerical dataframe
    new = pd.merge(numdf, categ_df, left_index=True, right_index=True)

    return new

#function to get statistical data
def Statnalysis(df):
    print("Numerical Attributes:")
    print(df.describe(include=[np.number]))
    print("Categorical Attributes:")
    print(df.describe(include=[np.object]))

    print("Bodystyles:", df.vehicleType.unique())
    print("Gearbox:", df.gearbox.unique())
    print("FuelType:", df.fuelType.unique())
    print("Damage:", df.notRepairedDamage.unique())

#function to transform a dataframe into a list of lists
def df_to_array(df):
    data = []
    headers = list(df)
    for idx, i in enumerate(df.iterrows()):

        datarow = []
        for idy, h in enumerate(headers):
            datarow.append(df.iloc[idx,idy])

        data.append(datarow)

    return data

