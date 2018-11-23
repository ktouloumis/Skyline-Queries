class CategPrep:

    results = {}

    #functions to assign partial order preference for categorical attributes
    def util_bodystyle(ls, label):
        bodydict = {}
        bodydict['coupe'] = (1, 2)
        bodydict['cabrio'] = (3, 4)
        bodydict['suv'] = (5, 6)
        bodydict['wagon'] = (7, 8)
        bodydict['limousine'] = (9, 10)
        bodydict['bus'] = (11, 12)
        bodydict['kombi'] = (13, 14)
        bodydict['other'] = (15, 16)
        CategPrep.results[label] = bodydict

    def util_gearbox(ls, label):
        gear = {}
        gear['manual'] = (1, 2)
        gear['automatic'] = (3, 4)
        CategPrep.results[label] = gear

    def util_fueltype(x, label):
        #['diesel' 'benzin' 'lpg' 'andere' 'hybrid' 'cng' 'elektro']
        fueldict = {}
        fueldict['diesel'] = (3, 4)
        fueldict['gas'] = (1,2)
        fueldict['lpg'] = (5, 6)
        fueldict['other'] = (7, 8)
        fueldict['hybrid'] = (9, 10)
        fueldict['cng'] = (11, 12)
        fueldict['elektro'] = (13, 14)
        CategPrep.results[label] = fueldict

    def util_Damage(ls, label):
        damage = {}
        damage['no'] = (1, 2)
        damage['yes'] = (3, 4)
        CategPrep.results[label] = damage

    #function to process categorical attributes of dataframe
    def CategPreprocess(df):
        headers = list(df)
        print(headers)
        dict = {}

        for h in headers:
            dict[h] = list(df[h].unique())

        print ("DICT = ",dict)


        v = dict['vehicleType']
        CategPrep.util_bodystyle(v, 'vehicleType')

        v = dict['gearbox']
        CategPrep.util_gearbox(v, 'gearbox')

        v = dict['fuelType']
        CategPrep.util_fueltype(v, 'fuelType')

        v = dict['notRepairedDamage']
        CategPrep.util_Damage(v, 'notRepairedDamage')

        #access values
        print("CLASS DICT = ", CategPrep.results)

        #change values in dataframe
        for idy, h in enumerate(headers):
            for idx, line in enumerate(df.iterrows()):

                val = df.iloc[idx, idy]
                df.iloc[idx, idy] = CategPrep.results[h][val]

        return df