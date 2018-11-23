import math

#function to process numerical attributes
def NumPreprocess(df):

    #get min and max for each numericalattribute
    headers = list(df)
    print("NUMERICAL HEADERS = ", headers)
    print("price:",df['price'].min(),"-",df['price'].max())
    print("powerPS :", df['powerPS'].min(), "-", df['powerPS'].max())
    print("kilometer:", df['kilometer'].min(), "-", df['kilometer'].max())
    print(len(df))

    #access dataframe old values and change them
    for idy, h in enumerate(headers):
        print(h)
        for idx, i in enumerate(df.iterrows()):

            val = df.iloc[idx,idy]
            if h=='price':
                new_val = util_num(val, 25000, 5000, 4, True, False)

            if h=='powerPS':
                new_val = util_num(val, 250, 50, 4, False, False)

            if h=='kilometer':
                new_val = util_num(val, 150000, 0, 3, True)

            df.iloc[idx, idy] = new_val
    print("Finished binning")

    return df

#utility function for numerical attribute
def util_num(val , max, min, bins, invert=False, covered = True ):

    norm = (float(val-min)/(max-min))*100
    dist = int(100)/bins
    cat = False

    for idx, i in enumerate(range(0,int(101-dist),int(dist)), 1):

        if norm<math.ceil(i+dist):
            Bin = idx
            cat = True
            break

    if cat == False:
        Bin = bins+1

    if not covered:
        bins = bins+1

    if (invert==True):
        Bin = bins+1-Bin

    return float(Bin)
