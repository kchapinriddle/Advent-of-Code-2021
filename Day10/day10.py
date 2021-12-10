# Day 10: Syntax Scoring

import statistics as st

# Part 1
# Problem Summary: On each _complete_ line, find the first mismatched closing symbol
# With )=3, ]=57, }=1197, >=25137, find the sum of mismatched closing symbols
# Part 2
# Problem Summary: On each _incomplete_ line, find the missing closing symbols
# For each closing symbol, score *=5 then + a point value: )=1, ]=2, }=3, >=4
# Find _median_ score

p1scoredict = {')':3,']':57,'}':1197, '>':25137}
p2scoredict = {')':1,']':2,'}':3, '>':4}
pairsdict = {'(':')',')':'(','[':']',']':'[','{':'}','}':'{','<':'>','>':'<'}
openings = ['(','[','{','<']

with open("input") as f:
    p1score = 0
    p2scores = []
    for line in f.readlines():
        l = line.strip()
        stack = [] # Holds _expected_ series of closing symbols
        corrupt = False
        # Use a stack to hold expected closing symbols, remove matched symbols
        for char in l:
            if char in openings: # Open a new chunk
                stack.append(pairsdict[char])
            else: # Close a chunk, or find corruption error
                if stack[-1] == char: # Close the chunk
                    stack.pop()
                else: # Otherwise found a corruption error
                    #print("Expected " + stack[-1] + ", but found " + char + " instead.")
                    corrupt = True
                    p1score += p1scoredict[char]
                    break # Go to next line
        # If not corrupt, score for incompletion
        if corrupt:
            continue
        score = 0
        stack.reverse() # Reverse to a queue to match expected order - eg printing order
        for char in stack:
            score *= 5
            score += p2scoredict[char]
        p2scores.append(score)
    
    
    print("P1: Score is " + str(p1score))
    print("P2: Score is " + str(st.median(p2scores)))
    
    

input("Enter to exit")