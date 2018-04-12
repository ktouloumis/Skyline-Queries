import csv
from sklearn.feature_extraction import DictVectorizer
import matplotlib.pyplot as plt
import pandas as pd

def width_util(w):
    if w < 64:
        width = 1
    elif w<68:
        width = 2
    else:
        width = 3
    return width

def height_util(h):
    if h < 54:
        height = 1

    else:
        height = 2
    return height

def price_util(pr):
    if pr < 10000:
        price = 1
    elif pr < 15000:
        price = 2
    elif pr < 20000:
        price = 3
    elif pr < 25000:
        price = 4
    else:
        price = 5
    return price

def doors_util(doors):
    if doors == 'two':
        num_of_doors = 2
    else:
        num_of_doors = 4

    return num_of_doors


def horsepower_util(hp):
    if hp < 50:
        horsepower = 1
    elif hp < 100:
        horsepower = 2
    elif hp < 150:
        horsepower = 3
    elif hp < 200:
        horsepower = 4
    else:
        horsepower = 5

    return horsepower

def compression_util(cmp):
    if cmp < 11:
        compression = 1
    elif cmp < 15:
        compression = 2
    elif cmp < 19:
        compression = 3
    else:
        compression = 4

    return compression

def length_util(l):
    if l < 160:
        length = 1
    elif l < 180:
        length = 2
    else:
        length = 3
    return length

class Auto(object):

    N = 1
    def __init__(self, doors, horse, pr, compr, length, width, height, fuel_type, eng_loc):
        self.index = Auto.N
        Auto.N = Auto.N + 1

        self.num_of_doors = doors_util(doors)

        self.horsepower = horsepower_util(horse)

        self.price = price_util(pr)

        self.compression = compression_util(compr)

        self.length = length_util(length)

        self.width = width_util(width)

        self.height = height_util(height)

        self.fuel_type = 2 if fuel_type== 'gas' else 1
        self.eng_loc = 2 if eng_loc=='front' else 1

    def print_self(self, letter = '0', xcord='0', ycord = '0'):
        print 'doors = %s, horsepower = %s, price = %s, compres = %s , l/w/h = %s/%s/%s' \
              % (self.num_of_doors, self.horsepower, self.price, self.compression, self.length, self.width,self.height)


def compare(a,b):
    #returns true if b dominates a
    cond1 = int(b.horsepower) >= int(a.horsepower)
    cond2 = int(b.price) < int(a.price)
    cond3 = int(b.num_of_doors) >= int(a.num_of_doors)
    cond4 = float(b.compression)>=float(a.compression)
    cond5 = float(b.height)>=float(a.height)
    cond6 = float(b.length)>=float(a.length)
    cond7 = b.fuel_type>=a.fuel_type

    return cond1 and cond2 and cond3 and cond4 and cond5 and cond6  and cond7


def Naive(list):
    skyline = []
    for a in list:
        flag = True
        for b in list:
            if (a != b):
                if compare(a, b):
                    print "%s dominating %s" % (b.index, a.index)
                    flag = False
        if flag == True:
            print "%s is DOMINANT" % a.index
            skyline.append(a)

    return skyline


idx = 0
list = []
vec = DictVectorizer()



with open('autos.csv') as csvfile:

    reader = csv.DictReader(csvfile)
    headers = reader.fieldnames
    print headers

    for row in reader:
        #dict =  {'num-of-doors': row['num-of-doors'], '' },
        #print row
        idx = idx + 1
        list.append({'num-of-doors':row['num-of-doors'], 'horsepower':int(row['horsepower']  if row['horsepower']!='?' else 150),
                     'price': int(row['price']) if row['price']!='?' else 10000, 'fuel-type':row['fuel-type'],
                     'engine-location':row['engine-location'], 'wheel-base':row['wheel-base'],
                     'length':float(row['length']), 'width':float(row['width']), 'height':float(row['height']),
                     'compression-ratio':row['compression-ratio']
                     })
        #print(row['num-of-doors'], row['horsepower'], row['price'])
        if idx==200:
            break

    cars = []
    for r in list:
        if r['price']!='?':
            a = Auto(r['num-of-doors'], r['horsepower'], r['price'], r['compression-ratio'], r['length'], r['width'], r['height'],
                     r['fuel-type'], r['engine-location'])
        else:
            a = Auto(r['num-of-doors'], r['horsepower'], 10000, r['compression-ratio'], r['length'], r['width'], r['height'],
                     r['fuel_type'], r['engine-location']
                     )
        #a.print_self()
        cars.append(a)

        # plot the points
    # plt.axis([100, 180, 0, 20000])
    # for p in cars:
    #     p.print_self()
    #     plt.plot(int(p.horsepower), int(p.price), 'ro')
    #     plt.annotate(p.index, (int(p.horsepower), int(p.price)))
    #
    # plt.show()

sk = Naive(cars)
print sk.__len__()

for it in sk:
    it.print_self()

vec.fit_transform(list).toarray()
print vec.get_feature_names()


df = pd.read_csv('autos.csv')
#print df.head()
#x =  df.describe()

# with open('out.txt', 'w') as f:
#     print >> f, x  # Python 2.x

#print df['horsepower']