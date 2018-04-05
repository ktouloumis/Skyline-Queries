import Point

def Naive(list):
    skyline = []
    for a in list:
        flag = True
        for b in list:
            if (a!=b):
                if Point.compare(a,b):
                    print "%s dominating %s" % (b.letter, a.letter)
                    flag = False
        if flag ==True:
            print "%s is DOMINANT" %a.letter
            skyline.append(a)

    return skyline