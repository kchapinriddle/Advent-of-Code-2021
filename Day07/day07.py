# Day 07: The Treachery of Whales

import statistics

# Part 1
# Problem Summary: Given a list, find the (or a) value such that sum(|entry - value|) is minimal. 
# Then output sum(|entry - value|)
# Part 2
# Now minimize sum(|entry-value|*(|entry-value|+1))/2

def p2sum(crabs, guess):
    sumerr = 0
    for c in crabs:
        sumerr += abs(c - guess)*(abs(c - guess)+1)/2
    return int(sumerr)

with open("input") as f:
    crabs = list(map(int,f.read().strip().split(',')))
    crabs.sort()
    
    # The median is a value that minimizes sum(|entry - value|). 
    # Though, if the median isn't in the list any value
    # on the range between the two entries flanking the median would work (inclusive)
    # which is why rounding via int() is A-OK
    # Follows from counting number of entries above/below chosen value
    # and noting that # above+including median is > # below and number #below+including
    # is > #above. 
    med = int(statistics.median(crabs))
    sumerr = 0
    for c in crabs:
        sumerr += abs(c - med)
    print("P1: " + str(sumerr))
    
    # The average would minimize sum(|entry-value|*|entry-value|), so that's a good start
    guess = int(statistics.mean(crabs))
    # Then do something like a binary sort based on slope to find minimum
    low = min(crabs)
    high = max(crabs)
    while True:
        if p2sum(crabs,guess) < p2sum(crabs,guess-1) and p2sum(crabs,guess) < p2sum(crabs,guess +1):
            print("P2: " + str(guess) + "  " + str(p2sum(crabs,guess)))
            break
        elif p2sum(crabs,guess) > p2sum(crabs,guess-1):
            print("Down!")
            high = guess - 1
            guess = int((guess + low)/2)
        elif p2sum(crabs,guess) > p2sum(crabs,guess+1):
            print("Up!")
            low = guess + 1
            guess = int((guess + high)/2)
    

input("Enter to exit")