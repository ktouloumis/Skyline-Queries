from itertools import islice
import Point

def next_n_lines(file_opened, N):
    return [x.strip() for x in islice(file_opened, N)]

def BlockNestedLoop(txt_name):
    print "Block Nested Loop"
    window = []
    with open(txt_name, 'r') as sample:
        line = next_n_lines(sample, 1)
        letter, xcord, ycord = line[0].split(",")
        p = Point.Point(letter, xcord, ycord)
        window.append(p)

        while line != []:
            # process line
            line = next_n_lines(sample, 1)
            for point in line:
                letter, xcord, ycord = point.split(",")

                p = Point.Point(letter, xcord, ycord)
                # process each point
                dom = False
                print "window:"
                for w in window:
                    print w.letter
                for it in window:
                    print "Comparing %s to %s" % (p.letter, it.letter)
                    cond1 = int(p.xcord) < int(it.xcord)
                    cond2 = int(p.ycord) < int(it.ycord)

                    if cond1 and cond2:
                        dom = True
                        print "dominant"
                    elif cond1 or cond2:
                        print "incomparable"
                        dom = True
                    else:
                        print "discarded"
                        dom = False
                        break
                if dom:
                    window.append(p)
    return window
