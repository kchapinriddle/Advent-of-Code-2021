# Day 22: Reactor Reboot

# Parts 1,2
# Problem Summary: 
# Infinite 3-grid of cells, each on or off
# Each line contains a command: "on" or "off" followed by the x y z range of a rectangular prism
# Execute each line in order, output number of cells "on" at end
# Part 1: Ignore anything outside [-50,50] on each axis
# Part 2: Do the whole thing

# TODID: It works! But too slowly
# Speed optimization - can adjacent "cuts" be glued together to keep command list from exploding?
# Or perhaps only make necessary divisions, so as to prevent explosive growth?
# Implemented: buffer not-overlapping segments, to prevent needless rechecking
#       90% reduction in runtime!
# Implemented: Don't store "off" commands after overlap is pruned - they've done their job
#       80% reduction in command list size!

import copy

code = {'n':1,'f':0}

def print_command(c):
    print("CMD: Set to",c[0], "x "+str(c[1])+".."+str(c[2]),  "y "+str(c[3])+".."+str(c[4]),  "z "+str(c[5])+".."+str(c[6]), "Command #", c[7])

def print_commands(lst):
    for command in lst:
        print_command(command)

def check_axis_overlap(c1l, c1h, c2l, c2h):
    if c2l <= c1l and c1l <= c2h:
        return True
    if c2l <= c1h and c1h <= c2h:
        return True
    if c1l <= c2l and c2l <= c1h:
        return True
    if c1l <= c2h and c2h <= c1h:
        return True
    return False

# Take two commands: if they intersect, return True
def check_intersection(c1,c2):
    if check_axis_overlap(c1[1],c1[2],c2[1],c2[2]): # Check x-axis
        if check_axis_overlap(c1[3],c1[4],c2[3],c2[4]): # Check y-axis
            if check_axis_overlap(c1[5],c1[6],c2[5],c2[6]): # Check z-axis
                return True
    return False

def single_overlap(c, command_set):
    for oc in command_set:
        if c==oc:
            continue
        elif c[1] == oc[1] and c[2] == oc[2] and c[3] == oc[3] and c[4] == oc[4] and c[5] == oc[5] and c[6] == oc[6]:
            if c[7] == oc[7]:
                print("ERROR: Two different commands with same bounds and command numbers")
                input("Enter to quit")
                exit()
            if c[7] < oc[7]:
                return []
    return [c]

def prune_overlap(command_set):
    return_commands = []
    for c in command_set:
        return_commands += single_overlap(c, command_set)
    return return_commands

def split_below(old_c, x, y, z):
    to_split = []
    did_split = [old_c.copy()]
    # Split on X axis
    if old_c[1] < x and x <= old_c[2]:
        to_split = did_split
        did_split = []
        for c in to_split:
            nc_low, nc_high = c.copy(), c.copy()
            nc_low[2], nc_high[1] = x-1, x
            did_split += [nc_low,nc_high]
    if old_c[3] < y and y <= old_c[4]:
        to_split = did_split
        did_split = []
        for c in to_split:
            nc_low, nc_high = c.copy(), c.copy()
            nc_low[4], nc_high[3] = y-1, y
            did_split += [nc_low,nc_high]
    if old_c[5] < z and z <= old_c[6]:
        to_split = did_split
        did_split = []
        for c in to_split:
            nc_low, nc_high = c.copy(), c.copy()
            nc_low[6], nc_high[5] = z-1, z
            did_split += [nc_low,nc_high]
    return did_split

def split_above(command, x, y ,z):
    return split_below(command, x+1, y+1, z+1)

def split_overlapping_commands(c1,c2):
    if not check_intersection(c1,c2):
        print("DBG:Attempted to split non-intersecting commands!")
        print_commands([c1,c2])
        exit()
    c1_split_a = split_below(c1, c2[1], c2[3], c2[5])
    c1_split_final = []
    for c in c1_split_a:
        c1_split_final += split_above(c, c2[2], c2[4], c2[6])
    c2_split_a = split_below(c2, c1[1], c1[3], c1[5])
    c2_split_final = []
    for c in c2_split_a:
        c2_split_final += split_above(c, c1[2], c1[4], c1[6])
    split_semi_final = c1_split_final + c2_split_final
    return prune_overlap(split_semi_final)

def subreactor_command(subset, c):
    new_command_num = c[7]
    for rc in subset:
        if check_intersection(rc,c):
            subset.remove(rc)
            spt = split_overlapping_commands(rc,c)
            for com in spt: # Reinsert old split commands
                if com[7] < new_command_num:
                    subset.append(com)
            for com in spt: # Recurse on splits of new command
                if com[7] == new_command_num:
                    subreactor_command(subset, com)
            return
    if c[0]:
        subset.append(c) # If no overlaps, make sure to append!

def new_reactor_command(reactor, c):
    subset = []
    for rc in reactor:
        if check_intersection(rc,c):
            subset.append(rc)
    for ss in subset:
        reactor.remove(ss)
    subreactor_command(subset,c)
    reactor += subset

# Old version which did not trim non-intersecting before rechecking subsplits
'''def reactor_command(reactor, c):
    new_command_num = c[7]
    for rc in reactor:
        if check_intersection(rc,c):
            reactor.remove(rc)
            spt = split_overlapping_commands(rc,c)
            for com in spt: # Reinsert old split commands
                if com[7] < new_command_num:
                    reactor.append(com)
            for com in spt: # Recurse on splits of new command
                if com[7] == new_command_num:
                    reactor_command(reactor, com)
            return
    if c[0]:
        reactor.append(c) # If no overlaps, make sure to append!'''

with open("input") as f:
    commands = []
    cubenum = 0 # Tracks order of instructions, for determining "winner" of overlap
    for line in f.readlines():
        l = line.strip()
        if l == "":
            break
        toggle = l[1] # 'n' for on, 'f' for off
        insts = l.split(' ')[1].split(',') # Results in chunks of "N=INT..INT"
        command = [code[toggle]]
        c = []
        for i in range(len(insts)):
            insts[i] = insts[i].split('=')[1] # Results in chunks of "INT..INT"
            c += insts[i].split("..")
        for i in c:
            command.append(int(i))
        command.append(cubenum)
        cubenum += 1
        commands.append(command)
    # Store reactor as list of commands
    new_reactor = []
    # Run commands in order
    for c in commands:
        print("Doing command #",c[7], "reactor size", len(new_reactor))
        new_reactor_command(new_reactor,c)
    cells_active = 0
    for c in new_reactor: # Hacky: Ignores anything outside bounds because input for part 1 never goes partially out of bounds
        if c[1] < -50 or c[2] > 50 or c[3] < -50 or c[4] > 50 or c[5] < -50 or c[6] > 50:
            continue
        cells_active += c[0] * (c[2]+1-c[1]) * (c[4]+1-c[3]) * (c[6]+1-c[5])
    print("Part 1:", cells_active)
    cells_active = 0
    for c in new_reactor:
        cells_active += c[0] * (c[2]+1-c[1]) * (c[4]+1-c[3]) * (c[6]+1-c[5])
    print("Part 2:", cells_active)


input("Enter to exit")