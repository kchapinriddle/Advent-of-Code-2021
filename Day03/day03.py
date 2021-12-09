# Day 03: Binary Diagnostic

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
# Problem summary: Given a file containing some number of bits (in text) per line,
# determine the most common value for the first bit, remove all values that do not match, 
# and repeat for remaining digits in order until only one value remains.
# Then repeat for least common value. 
# Then return product of results

bitlen = 0
with open("input") as f:
    bitlen = len(f.readline().strip())

# Most common pass
oxygen = 0
with open("input") as f:
    lines = f.read().splitlines()
    for i in range(bitlen):
        bit = 0
        # Find most common bit
        for l in lines:
            if l[i] == '1':
                bit += 1
            else:
                bit -= 1
        if bit >= 0:
            bit = 1
        else:
            bit = 0
        
        # Remove mismatches
        lines = [l for l in lines if l[i] == str(bit)]
        if len(lines) == 1:
            break
    oxygenbits = lines[0]
    value = pow(2,bitlen-1)
    for i in range(bitlen):
        oxygen += value * int(oxygenbits[i])
        value /= 2

# Least common pass
co2 = 0
with open("input") as f:
    lines = f.read().splitlines()    
    for i in range(bitlen):
        bit = 0
        # Find least common bit
        for l in lines:
            if l[i] == '1':
                bit += 1
            else:
                bit -= 1
        if bit >= 0:
            bit = 0
        else:
            bit = 1
        
        # Remove mismatches
        lines = [l for l in lines if l[i] == str(bit)]
        if len(lines) == 1:
            break
    co2bits = lines[0]
    value = pow(2,bitlen-1)
    for i in range(bitlen):
        co2 += value * int(co2bits[i])
        value /= 2
print("Oxy: " + str(oxygen) + ' ' + "CO2: " + str(co2))
print(str(oxygen * co2))

input("Enter to exit")