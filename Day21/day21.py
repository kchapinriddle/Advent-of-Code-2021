# Day 21: Dirac Dice

# Parts 1,2
# Problem Summary: 
# Circular array [10] containing 1-10, used as game board.
# Each turn, player rolls thrice and advances that many spaces,
# adding their new space's number to their score
# Part 1: Use d100 that counts up from 1 deterministically
# Winner is whoever reaches score of 1000 first, return number of rolls times loser's score
# Part 2: use d3, evaluate _all possible outcomes_, return higher number of wins ("multiverses")

# Part 1
def get_roll(die):
    die[1] += 1
    die[0] += 1
    if die[0] > 100:
        die[0] -= 100
    return die[0]

def get_3_rolls(die):
    return get_roll(die) + get_roll(die) + get_roll(die)

def do_turn(die,position,score):
    position += get_3_rolls(die)
    position = position % 10
    if position == 0:
        position = 10
    score += position
    return position, score

with open("input") as f:
    # Read in player starting positions, set initial state
    p1pos = int(f.readline().strip().split(' ')[-1])
    p2pos = int(f.readline().strip().split(' ')[-1])
    die = [0,0] # Current facet, number of rolls
    p1score = 0
    p2score = 0
    while True: 
        p1pos, p1score = do_turn(die,p1pos,p1score)
        if p1score >= 1000:
            print("Part 1:",p2score*die[1])
            break
        p2pos, p2score = do_turn(die,p2pos,p2score)
        if p2score >= 1000:
            print("Part 1:",p1score*die[1])
            break

# Part 2
with open("input") as f:
    die = [[3,1],[4,3],[5,6],[6,7],[7,6],[8,3],[9,1]] # Die result, num times it occurs in 3d3
    # Read in player starting positions, set initial state
    p1pos = int(f.readline().strip().split(' ')[-1])-1
    p2pos = int(f.readline().strip().split(' ')[-1])-1
    # Store states as 4-tuples: (p1pos p1score p2pos p2score)
    # Use as keys to a dict containing how many of that state exist
    initial_state = (p1pos, 0, p2pos, 0)
    states = {initial_state:1}
    wins = [0,0]
    turn = 0
    while True:
        turn += 1
        print("Doing turn",turn)
        # P1 turn
        old_states = states
        states = {}
        for st in list(old_states):
            for res in die:
                if st[1]+(st[0]+res[0])%10+1 >= 21:
                    wins[0] += old_states[st] * res[1]
                else:
                    nst = ((st[0]+res[0])%10, st[1]+(st[0]+res[0])%10+1, st[2], st[3])
                    if nst in list(states):
                        states[nst] = states[nst] + old_states[st] * res[1]
                    else:
                        states[nst] = old_states[st] * res[1]
        # P2 turn
        old_states = states
        states = {}
        for st in list(old_states):
            for res in die:
                if st[3]+(st[2]+res[0])%10+1 >= 21:
                    wins[1] += old_states[st] * res[1]
                else:
                    nst = (st[0], st[1], (st[2]+res[0])%10, st[3]+(st[2]+res[0])%10+1)
                    if nst in list(states):
                        states[nst] = states[nst] + old_states[st] * res[1]
                    else:
                        states[nst] = old_states[st] * res[1]
        if states == {}:
            break
    print("Part 2:",max(wins))

input("Enter to exit")