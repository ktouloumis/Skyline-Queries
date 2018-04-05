import Naive
import Point

def Divide_and_Conquer(list):
    # Devide and conquer
    sumx = sumy = 0

    for point in list:
        sumx = sumx + int(point.xcord)
        sumy = sumy + int(point.ycord)

    medianx = sumx / len(list)
    mediany = sumy / len(list)

    print "Medianx = %s and Mediany = %s" % (medianx, mediany)
    p11 = []
    p12 = []
    p21 = []
    p22 = []

    for point in list:
        if (int(point.xcord) <= medianx and int(point.ycord) >= mediany):
            p12.append(point)
        elif (int(point.xcord) <= medianx and int(point.ycord) < mediany):
            p11.append(point)
        elif (int(point.xcord) > medianx and int(point.ycord) < mediany):
            p21.append(point)
        elif (int(point.xcord) > medianx and int(point.ycord) >= mediany):
            p22.append(point)

    sk11 = Naive.Naive(p11)
    print "Skyline of P11"
    for item in sk11:
        print item.letter

    sk12 = Naive.Naive(p12)
    print "Skyline of P12"
    for item in sk12:
        print item.letter

    sk22 = Naive.Naive(p22)
    print "Skyline of P22"
    for item in sk22:
        print item.letter

    sk21 = Naive.Naive(p21)
    print "Skyline of P21"
    for item in sk21:
        print item.letter

    skyline = []
    skyline = skyline + sk11

    sk1 = Naive.Naive(sk11 + sk12 + sk21)

    return sk1