# Day 08: Seven Segment Search

# Part 1
# Problem Summary: Given ten strings representing the segments active for each of the 
# segments of each digit in a seven-segment display, but in no particular order or standard meaning
# decipher four strings of output
# For now, just output the number of 1s, 4s, 7s, 8s in the "output" section

with open("input") as f:
    uniques = 0
    while True:
        # Extract output digits
        outdigits = f.readline().strip().split('|')
        if outdigits == ['']:
            break # If EOF, done
        outdigits = outdigits[1].split()
        # Now count based on length
        for i in outdigits:
            if len(i) in [2,3,4,7]:
                uniques += 1
    print("P1: " + str(uniques) + " 1s, 4s, 7s, 8s in output")

# Part 2
# Fully decode, output sum of all "output" section values
with open("input") as f:
    total = 0
    for line in f.readlines():
        strNums = {}
        indigits, outdigits = line.strip().split('|')
        indigits, outdigits = indigits.split(), outdigits.split()
        # Identify 1, 4, 7, 8
        for i in indigits:
            if len(i) == 2: # 2-seg means it's 1
                strNums[1] = i
                strNums[i] = 1
            if len(i) == 3: # 3-seg means it's 7
                strNums[7] = i
                strNums[i] = 7
            if len(i) == 4: # 4-seg means it's 4
                strNums[4] = i
                strNums[i] = 4
            if len(i) == 7: # 7-seg means it's 1
                strNums[8] = i
                strNums[i] = 8
        # Identify 3, 5, then 2
        for i in [x for x in indigits if len(x) == 5]: # If it's 5-seg,
            if strNums[1][0] in i and strNums[1][1] in i: # and it's got 1's segs,
                strNums[3] = i # then it's 3
                strNums[i] = 3
            else:
                miss = strNums[4]
                for char in i:
                    miss = miss.replace(char, '')
                if len(miss) == 1: # and it's missing only one of 4's segs,
                    strNums[5] = i # then it's 5
                    strNums[i] = 5
        for i in [x for x in indigits if len(x) == 5]: # And there's only three 5-seg digits,
            if i != strNums[3] and i != strNums[5]: # so if it's not 3 or 5,
                strNums[2] = i # then it's 2
                strNums[i] = 2
        # Identify 9
        for i in [x for x in indigits if len(x) == 6]: # If it's 6-seg,
            nineset = set(strNums[4]).union(set(strNums[5]))
            if set(i) == nineset: # and it has all the segments in 4 and 5,
                strNums[9] = i # then it's 9
                strNums[i] = 9
        # Identify 6, 0
        for i in [x for x in indigits if len(x) == 6]: # If it's 6-seg,
            if i == strNums[9]: 
                continue # and isn't 9,
            if strNums[1][0] in i and strNums[1][1] in i: # and it's got 1's segs,
                strNums[0] = i # then it's 0
                strNums[i] = 0
            else:
                strNums[6] = i # otherwise it's 6
                strNums[i] = 6
        
        # Check we've got them all
        if len(list(strNums)) != 20:
            print("ERROR: Missed digits in input:")
            print(indigits)
        
        # Start summing
        outval = 0
        for i in outdigits:
            for j in list(strNums):
                if type(j) == int:
                    continue #Wrong type of key, disregard
                if set(i) == set(j):
                    outval *= 10
                    outval += strNums[j]
        total += outval
        
    print("P2 sum: " + str(total))

input("Enter to exit")