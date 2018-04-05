import math
class Point(object):
    N = 16
    def __init__(self, name, x, y):
        self.letter = name
        self.xcord = x
        self.ycord = y

    def print_self(self, letter = '0', xcord='0', ycord = '0'):
        print 'letter = %s, xcord = %s, ycord=%s ' % (self.letter, self.xcord, self.ycord)

    def eucl(self):
        return math.sqrt( pow(int(self.xcord),2)+ pow(int(self.ycord),2)  )

def compare(a,b):
    #returns true if b dominates a
    cond1 = int(b.xcord) < int(a.xcord)
    cond2 = int(b.ycord) < int(a.ycord)
    return cond1 and cond2