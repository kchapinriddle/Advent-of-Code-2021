# Day 14: Extended Polymerization

# Parts 1,2
# Problem Summary: Input contains a string on the first line, blank second line,
# replacement rules on future lines in format AB -> C
# Replacement replaces AB with ACB, all instances simultaneous
# Part 1: Run 10 loops, output (most common character - least common character)
# Part 1: Run 40 loops, output (most common character - least common character)

def get_result(poly, part, lastchar, maxval):
    # Get the first in each pair, condense
    pcount = {}
    for i in set(poly):
        if not i[0] in pcount:
            pcount[i[0]] = 0
        pcount[i[0]] += poly[i]
    pcount[lastchar] += 1
    # Find most common, least common, difference
    maxmin = [0,maxval]
    for i in set(pcount):
        maxmin[0] = max(maxmin[0], pcount[i])
        maxmin[1] = min(maxmin[1], pcount[i])
    print("Part " + part + ": " +str(maxmin[0]-maxmin[1]))

with open("input") as f:
    poly = {}
    # Read in starting state
    startpoly = f.readline().strip()
    lastchar = startpoly[-1]
    for i in range(len(startpoly)-1):
        pair = startpoly[i]+startpoly[i+1]
        if not pair in poly:
            poly[pair] = 0
        poly[pair] = poly[pair] + 1
    f.readline() # Discard the blank line
    # Set up dict of replacements
    replacements = {}
    for line in f.readlines():
        l = line.strip().split(" -> ")
        replacements[l[0]] = [l[0][0] + l[1], l[1] + l[0][1]]
    
    goal = 40
    for loop in range(1,goal+1):
        oldpoly = poly
        poly = {}
        for i in replacements:
            if i in oldpoly:
                if not replacements[i][0] in poly:
                    poly[replacements[i][0]] = 0
                if not replacements[i][1] in poly:
                    poly[replacements[i][1]] = 0
                poly[replacements[i][0]] += oldpoly[i]
                poly[replacements[i][1]] += oldpoly[i]
        # Output results
        if loop == 10:
            get_result(poly,"1",lastchar,len(startpoly)*pow(2,loop))
        if loop == 40:
            get_result(poly,"2",lastchar,len(startpoly)*pow(2,loop))
            

# Too slow for part 2, needs to be faster - can't be linear with respect to length, can't store string
'''def get_result(poly, part):
    maxmin = [0,len(poly)]
    for i in set(poly):
        maxmin[0] = max(maxmin[0], poly.count(i))
        maxmin[1] = min(maxmin[1], poly.count(i))
    print("Part " + part + ": " +str(maxmin[0]-maxmin[1]))

with open("input") as f:
    # Read in starting state
    poly = f.readline().strip()
    f.readline() # Discard the blank line
    # Set up dict of replacements
    replacements = {}
    for line in f.readlines():
        l = line.strip().split(" -> ")
        replacements[l[0][0] + '_' + l[0][1]] = l[0][0] + l[1] + l[0][1]
    loop = 0
    goal = 40
    while loop < goal:
        for i in set(poly):
            poly = poly.replace(i, i+"_")
        for i in replacements:
            # Have to do it twice to catch triples
            poly = poly.replace(i,replacements[i]).replace(i,replacements[i])
        poly = poly.replace("_","")
        loop += 1
        if loop == 10:
            get_result(poly, "1")
        if loop == 40:
            get_result(poly, "2")
        print(loop)'''

input("Enter to exit")