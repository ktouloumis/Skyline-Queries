from __future__ import division
import matplotlib.pyplot as plt
import Point
import Naive
import itertools
import BlockNestedLoop as BL
import Divide_and_Conquer as DC

if __name__ == '__main__':
    #open file to read points
    file = open("points.txt","r")

    #list to save the points
    list = []
    for line in file:
        #split lines with ',' as delimiter
        letter, xcord, ycord = line.split(",")

        #create new point
        p = Point.Point(letter, xcord, ycord)

        #p.print_self()

        #append point to list
        list.append(p)

    #plot the points
    plt.axis([0, 25, 0, 25])
    for p in list:
        #p.print_self()
        plt.plot(int(p.xcord),int(p.ycord),'ro')
        plt.annotate(p.letter, (int(p.xcord),int(p.ycord)))
    plt.show()

    #compute skyline set using naive algorithm
    print "Skyline Set:"

    newsk = Naive.Naive(list)
    for item in newsk:
        print item.letter

    #plot the skyline set along all points
    plt.axis([0, 25, 0, 25])
    for p in list:
        # p.print_self()
        plt.plot(int(p.xcord), int(p.ycord), 'ro')
        plt.annotate(p.letter, (int(p.xcord), int(p.ycord)))

    xs = []
    ys = []
    for p in newsk:
        xs.append(int(p.xcord))
        ys.append(int(p.ycord))

    plt.plot(xs, ys)
    plt.show()

    #END OF NAIVE

    #Block Nested Loop
    window = BL.BlockNestedLoop("points.txt")

    print "Skyline Set(Items in window)"
    for item in window:
        print item.letter

    #Divide and conquer
    sk = DC.Divide_and_Conquer(list)
    print "Skyline set by Divide and Conquer"
    for item in sk:
        print item.letter
