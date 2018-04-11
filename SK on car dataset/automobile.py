#utility functions for each attribute
def price_util(bp):
    if bp=='low':
        price = 1
    elif bp=='med':
        price = 2
    elif bp=='high':
        price = 3
    else:
        price = 4
    return price

def doors_util(d):

    if d=='5more':
        doors = 5
    else:
        doors = int(d)

    return doors

def capacity_util(c):
    if c == 'more':
        cap = 5
    else:
        cap = int(c)
    return cap

def lug_util(l):
    if l=='small':
        size = 1
    elif l=='med':
        size = 2
    elif l=='big':
        size = 3
    return size

def safety_util(s):
    if s=='low':
        safety = 1
    elif s=='med':
        safety = 2
    elif s=='high':
        safety = 3
    return safety

class Car:
    N = 1
    def __init__(self, bp, mp, d, pers, lug, safe):
        self.index = Car.N
        Car.N = Car.N + 1
        self.buy_price = price_util(bp)
        self.maint_price = price_util(mp)
        self.num_doors = doors_util(d)
        self.capacity = capacity_util(pers)
        self.size_lug = lug_util(lug)
        self.safety = safety_util(safe)

    def print_car(self):
        print "idx = %s, Buy pr = %s, Maint pr = %s, doors = %s" %(self.index, self.buy_price, self.maint_price, self.num_doors)

        print "Capac = %s, Luggage = %s, safety = %s \n" %(self.capacity, self.size_lug, self.safety)


def compare(a,b):
    #returns true if b dominates a
    cond1 = b.buy_price < a.buy_price
    cond2 = b.maint_price < a.maint_price
    cond3 = b.num_doors >= a.num_doors
    cond4 = b.capacity >= a.capacity
    cond5 = b.size_lug >= a.size_lug
    cond6 = b.safety >= b.safety

    return cond1 and cond2 and cond3 and cond4 and cond5 and cond6


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


if __name__ == "__main__":
    cars = []
    with open('car.data') as dat:

        for row in dat:
            vals = row.split(',')
            c = Car(vals[0], vals[1], vals[2], vals[3], vals[4], vals[5])
            cars.append(c)


    sk = Naive(cars)
    print sk.__len__()
