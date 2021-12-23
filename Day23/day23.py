# Day 23: Amphipod

# Parts 1,2
# Problem Summary: 
# Defies easy summary, see problem statements

# Approach: Keep list of states, ordered by descending energy cost
# Iteratively pop from rear, append all possible moves, sort by energy cost
# Once a solved state is popped, it's the best solution

import copy

e_costs = {'A':1,'B':10,'C':100,'D':1000}
room_keys = {0:'A', 'A':0, 1:'B', 'B':1, 2:'C', 'C':2, 3:'D', 'D':3}
gamestates = []
didstates = {}
m_cef = {}
m_clt = {}

def get_en(gs):
    return gs.energy

def add_if_not_there(gs):
    global gamestates
    for state in gamestates:
        if state.equals(gs):
            break
    else:
        gamestates.append(gs)

class gamestate:
    def __init__(self, initstr):
        self.energy = 0
        self.hall = ['.']*11
        start = []
        self.rooms = []
        if initstr != "":
            for c in initstr:
                if c in "ABCD":
                    start.append(c)
            self.rooms = [[start[0],start[4]],[start[1],start[5]],[start[2],start[6]],[start[3],start[7]]]
    
    # TODO test
    def is_solved(self):
        order = ['A','B','C','D']
        for i in range(4):
            for c in self.rooms[i]:
                if c != order[i]:
                    return False
        return True
    
    # Inputs:
    # int hdi (hall destination index)
    # int rsi (room source index)
    # int rsd (room source depth - how far in is mover)
    # Returns: int energy cost if move possible, else returns 0
    def can_leave_to(self, hdi, rsi, rsd):
        idc = str(self)+str(hdi)+str(rsi)+str(rsd)
        if (idc) in m_clt:
            return m_clt[idc]
        if self.rooms[rsi][rsd] == '.': # Can't move an empty space
            return 0
        for i in range(rsd+1, len(self.rooms[0])): # Ensure not leaving final destination
            if self.rooms[rsi][i] != room_keys[rsi]:
                break
        else:
            if self.rooms[rsi][rsd] == room_keys[rsi]:
                return 0
        if hdi in [2,4,6,8]: # Cannot stop above a room
            return 0
        for i in range(rsd): 
            if self.rooms[rsi][i] != '.': # Can't move through others in room
                return 0
        hallout = rsi * 2 + 2
        for i in range( min(hallout, hdi), max(hallout, hdi)+1 ): # Can't move through others in hall
            if self.hall[i] != '.':
                return 0
        evalue = e_costs[self.rooms[rsi][rsd]] * (rsd + abs(hallout - hdi) + 1)
        m_clt[idc] = evalue
        return evalue
    
    # Inputs:
    # int hsi (hall source index)
    # int rdi (room destination index)
    # int rdd (room destination depth - how far in is target)
    # Returns: int energy cost if move possible, else returns 0
    def can_enter_from(self, hsi, rdi, rdd):
        idc = str(self)+str(hsi)+str(rdi)+str(rdd)
        if (idc) in m_cef:
            return m_cef[idc]
        if self.hall[hsi] == '.': # Can't move an empty space
            return 0
        if self.rooms[rdi][rdd] != '.': # Can't move into filled space
            return 0
        if rdi != room_keys[self.hall[hsi]]: # Can't enter wrong room
                return 0
        for i in range(rdd+1, len(self.rooms[0])): # Ensure entering final destination
            if self.rooms[rdi][i] != room_keys[rdi]:
                return 0
        hallin = rdi * 2 + 2
        for i in range( min(hallin, hsi), max(hallin, hsi)+1 ): # Can't move through others in hall
            if self.hall[i] != '.' and i != hsi:
                return 0
        for i in range(rdd):
            if self.rooms[rdi][rdd] != '.': # Can't move through others in room
                return 0
        evalue = e_costs[self.hall[hsi]] * (rdd + abs(hallin - hsi) + 1)
        m_cef[idc] = evalue
        return evalue
    
    def __str__(self):
        st = ""
        for c in self.hall:
            st += c
        for i in range(len(self.rooms[0])):
            st += "\n #"
            for r in range(len(self.rooms)):
                st += self.rooms[r][i] + '#'
            st += ' '
        return st

    def copy(self):
        cpy = gamestate("")
        cpy.energy = self.energy
        cpy.hall = self.hall.copy()
        cpy.rooms = copy.deepcopy(self.rooms)
        return cpy

    # Check if any pieces can be moved to final locations
    def next_final_states(self):
        found_move = 0
        for hi in [0,1,3,5,7,9,10]:
            if self.hall[hi] == '.':
                continue
            ri = room_keys[self.hall[hi]]
            for rd in reversed(range(len(self.rooms[ri]))):
                cst = self.can_enter_from(hi,ri,rd)
                if cst != 0:
                    found_move += 1
                    n = self.copy()
                    n.hall[hi], n.rooms[ri][rd] = n.rooms[ri][rd], n.hall[hi]
                    n.energy += cst
                    gamestates.append(n)
                    break
        return found_move
    
    # Generate other next states
    def next_nonfinal_states(self):
        for hi in [0,1,3,5,7,9,10]:
            for ri in range(len(self.rooms)):
                for rd in range(len(self.rooms[ri])):
                    cst = self.can_leave_to(hi,ri,rd)
                    if cst > 0:
                        n = self.copy()
                        n.hall[hi], n.rooms[ri][rd] = n.rooms[ri][rd], n.hall[hi]
                        n.energy += cst
                        gamestates.append(n)
                    cst = self.can_enter_from(hi,ri,rd)
                    if cst > 0:
                        n = self.copy()
                        n.hall[hi], n.rooms[ri][rd] = n.rooms[ri][rd], n.hall[hi]
                        n.energy += cst
                        gamestates.append(n)

    # self should already be removed from global gamestates
    def next_states(self):
        #print("DBG", self.energy)
        global gamestates
        global didstates
        if str(self) in didstates: # Don't redo with worse numbers
            if didstates[str(self)] <= self.energy:
                return
        # Add possible following states, checking for final location moves first
        if self.next_final_states() == 0:
            self.next_nonfinal_states()
        # Prune out self, processing done. Sort. 
        didstates[str(self)] = self.energy
        gamestates.sort(reverse = True, key = get_en)
        

with open("input") as f:
    initial_state = gamestate(f.read())
    gamestates.append(initial_state)
    print("Running part 1, this will take a bit.")
    i = 0
    while True:
        if gamestates[-1].is_solved():
            break
        else:
            nxt = gamestates.pop()
            nxt.next_states()
        '''i += 1
        if i % 10000 == 0:
            print(i, gamestates[-1].energy)
            print(gamestates[-1])'''
    p1 = gamestates[-1].energy
    
    # Part 2, resetting and inserting new rows
    gamestates = []
    didstates = {}
    m_cef = {}
    m_clt = {}
    for r in initial_state.rooms:
        r.append(r[-1])
        r.append(r[-1])
    initial_state.rooms[0][1], initial_state.rooms[0][2] = 'D', 'D'
    initial_state.rooms[1][1], initial_state.rooms[1][2] = 'C', 'B'
    initial_state.rooms[2][1], initial_state.rooms[2][2] = 'B', 'A'
    initial_state.rooms[3][1], initial_state.rooms[3][2] = 'A', 'C'
    gamestates.append(initial_state)
    print("Running part 2, this will take longer.")
    i = 0
    while True:
        if gamestates[-1].is_solved():
            break
        else:
            nxt = gamestates.pop()
            nxt.next_states()
        '''i += 1
        if i % 10000 == 0:
            print(i, gamestates[-1].energy)
            print(gamestates[-1])'''
    print("Part 1:",p1)
    print("Part 2:",gamestates[-1].energy)
    
    '''test_state = gamestate("")
    test_state.hall = ['A','.','.','C','.','D','.','.','.','D','B']
    test_state.rooms = [['B','A'],['.','.'],['.','C'],['.','.']]
    print(test_state)
    print()
    test_state.next_states()
    for gs in gamestates:
        print(gs)'''

input("Enter to exit")