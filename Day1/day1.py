# Day 1: Sonar Sweep

# Part 1
# Problem summary: Given a file containing one int per line,
# output the number of lines which are larger than the previous line
increased = 0
with open("input") as f:
    i = 0
    j = int(f.readline().strip())
    for line in f:
        i = j
        j = int(line.strip())
        if i < j:
            increased += 1
    print(increased)

# Part 2
# Problem summary: Given a file containing one int per line,
# output the number of instances of the sum of the line and the two before it
# increasing relative to the sum of the last three lines
increased = 0
with open("input") as f:
    i = 0
    j = int(f.readline().strip())
    k = int(f.readline().strip())
    l = int(f.readline().strip())
    for line in f:
        i = j
        j = k
        k = l
        l = int(line.strip())
        if i < l: # because j and k are in both windows, they can be ignored
            increased += 1
    print(increased)

input("Enter to exit")