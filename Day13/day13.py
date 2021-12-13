# Day 13: Transparent Origami

# Parts 1,2
# Problem Summary: Input contains ordered pairs in an x,y notation
# Input then contains a blank line, and then fold instructions "fold along [x,y]=[#]"
# Place dots according to instruction, then "fold" along indicated line
# Part 1: Return number of dots after first fold
# Part 2: Print dots, revealing a text string

def mirror(point, line):    
    return line - (point - line)

def do_fold(xy, line, points):
    if xy == "x":
        xy = 0
    else:
        xy = 1
    for i in range(len(points)):
        if points[i][xy] > line:
            points[i][xy] = mirror(points[i][xy], line)

def print_part1(points):
    ndpoints = []
    for p in points:
        if not p in ndpoints:
            ndpoints.append(p)
    print("Part 1: ",len(ndpoints))

with open("input") as f:
    points = []
    folds = 0
    for line in f.readlines():
        if "," in line: # It's coords
            l = line.strip().split(",")
            points.append([int(l[0]),int(l[1])])
        if "f" in line: # It's a fold
            l = line.strip().split("=")
            do_fold(l[0][-1],int(l[1]),points)
            if folds == 0:
                print_part1(points)
            folds += 1
    # And remove duplicates
    ndpoints = []
    maxp = [0,0]
    for p in points:
        if not p in ndpoints:
            ndpoints.append(p)
            maxp[0] = max(maxp[0],p[0])
            maxp[1] = max(maxp[1],p[1])
    print("Part 2")
    for y in range(maxp[1]+1):
        for x in range(maxp[0]+1):
            if [x,y] in ndpoints:
                print("#",end="")
            else:
                print(" ",end="")
        print()

input("Enter to exit")