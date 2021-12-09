# Day 1: Binary Diagnostic

# Part 1
# Problem summary: Given a file containing some number of bits (in text) per line,
# determine the most and least common state per bit position
# use these to create two binary numbers, and return their product

# Get length, set up bit tracker
bits = []
with open("input") as f:
    inbits = f.readline().strip()
    for i in inbits:
        bits.append(0)

gamma = 0
with open("input") as f:
    for line in f:
        inbits = line.strip()
        for i in range(len(bits)): #sum per column, taking 0 as -1
            if inbits[i] == '0':
                bits[i] -= 1
            if inbits[i] == '1':
                bits[i] += 1
    
    print(bits)
    
    for i in range(len(bits)): #convert to 0/1 based on sign
        if bits[i] > 0:
            bits[i] = 1
        if bits[i] < 0:
            bits[i] = 0
    
    value = pow(2,len(bits)-1)
    for i in range(len(bits)):
        gamma += value * bits[i]
        value /= 2
    epsilon = pow(2,len(bits))-1 - gamma
    
    print(bits)
    print("Gamma " + str(gamma))
    print("Epsilon " + str(epsilon))
    print(str(gamma*epsilon))

# Part 2
# Problem summary: 

input("Enter to exit")