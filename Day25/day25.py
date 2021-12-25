# Day 25: Sea Cucumber

# Parts 1,2
# Problem Summary: 
# Input is grid of '.', '>', 'v'. '.' is empty space, others are movers. 
# Each step, first all '>'s move east if possible, then all 'v's move south if possible.
# All moves done in parallel, based on current empty space. ".>>." becomes ".>.>", not "..>>"
# Grid wraps around
# Part 1: Find first step on which no movers move
# Part 2: No part 2

import copy
didmove = 1

def next_coords(grid, y, x):
    ret = [y,x]
    if grid[y][x] == '>':
        ret[1] += 1
        if ret[1] >= len(grid[0]):
            ret[1] = 0
    elif grid[y][x] == 'v':
        ret[0] += 1
        if ret[0] >= len(grid):
            ret[0] = 0
    if grid[ret[0]][ret[1]] == '.':
        return ret
    else:
        return [y,x]

def do_move(grid, oldgrid, y, x):
    nxt = next_coords(oldgrid, y, x)
    if nxt == [y,x]:
        return
    else: 
        global didmove
        didmove = 1
        grid[y][x], grid[nxt[0]][nxt[1]] = grid[nxt[0]][nxt[1]], grid[y][x]

def update_grid_east(grid):
    oldgrid = copy.deepcopy(grid)
    for y in range(len(oldgrid)):
        for x in range(len(oldgrid[0])):
            if grid[y][x] == '>':
                do_move(grid, oldgrid, y, x)

def update_grid_south(grid):
    oldgrid = copy.deepcopy(grid)
    for y in range(len(oldgrid)):
        for x in range(len(oldgrid[0])):
            if grid[y][x] == 'v':
                do_move(grid, oldgrid, y, x)

def update_grid(grid):
    global didmove
    didmove = 0
    update_grid_east(grid)
    update_grid_south(grid)

with open("input") as f:
    grid = []
    for line in f.readlines():
        l = line.strip()
        grid.append(list(l))
    
    step = 0
    while didmove == 1:
        update_grid(grid)
        step += 1
    
    '''for row in grid:
        for cell in row:
            print(cell, end='')
        print()'''
    print("Part 1:",step)

input("Enter to exit")