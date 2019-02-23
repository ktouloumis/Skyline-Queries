from __future__ import division
import matplotlib.pyplot as plt
import Point
import Naive
import itertools
import BlockNestedLoop as BL
#import Divide_and_Conquer as DC

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
    plt.xlabel("Price (€/month)")
    plt.ylabel("Distance from city centre")
    plt.title("Rooms for rent in Delft")
    plt.axis([0, 1800, 0, 1500])
    for p in list:
        #p.print_self()
        print(p.xcord,p.ycord)
        plt.plot(float(p.xcord),float(p.ycord),'go')
        strpos = None
        strpos = "("+str(float(p.xcord))+","+str(float(p.ycord))+')'
        fstr = p.letter
        print ("strpos=",fstr)

        plt.annotate(fstr, (float(p.xcord)+10,float(p.ycord)+10))
    plt.savefig('room.png')
    plt.show()

    #compute skyline set using naive algorithm
    print ("Skyline Set:")

    newsk = Naive.Naive(list)
    for item in newsk:
        print (item.letter)

    #plot the skyline set along all points
    plt.xlabel("Price (€/month)")
    plt.ylabel("Distance from city centre (m)")
    plt.title("Rooms for rent in Delft")
    plt.axis([0, 1800, 0, 1500])
    for p in list:
        # p.print_self()
        plt.plot(float(p.xcord), float(p.ycord), 'go')
        plt.annotate(p.letter, (float(p.xcord)+10, float(p.ycord)+10))

    xs = []
    ys = []
    for p in newsk:
        xs.append(float(p.xcord))
        ys.append(float(p.ycord))

    plt.plot(xs, ys)
    plt.savefig('rooms.png')
    plt.show()

    #END OF NAIVE

    #Block Nested Loop
    window = BL.BlockNestedLoop("points.txt")

    print ("Skyline Set(Items in window)")
    for item in window:
        print (item.letter)

    #Divide and conquer
    # sk = DC.Divide_and_Conquer(list)
    # print ("Skyline set by Divide and Conquer")
    # for item in sk:
    #     print (item.letter)
