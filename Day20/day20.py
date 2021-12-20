# Day 20: Trench Map

# Parts 1,2
# Problem Summary: 
# First line of input is a set of '.'s and '#'s representing an array of 0s and 1s
# then a blank line
# Then a grid of '.'s and '#'s
# Each loop, expand the grid by 1 '.' in each direction, take each cell and its eight neighbors,
# and read in the '.'s and '#'s as 0s and 1s (left-right by rows from top-bottom). 
# Evaluate the 9-digit binary string as an int, use it as index to the array, that's the value post loop
# All updates parallel
# Part 1: Output number of '#'s after two updates
# Part 2: Output number of '#'s after fifty updates

import copy

def print_grid(grid):
    ot = {0:'.',1:'#'}
    for row in grid:
        for cell in row:
            print(ot[cell], end='')
        print()
    print()

def output_part(grid,part):
    gridsum = 0
    for row in grid:
        for cell in row:
            gridsum += cell
    print("Part "+part+":",gridsum)

def get_from_array(array,ninebits):
    idx = 0
    for bit in ninebits:
        idx *= 2
        idx += bit
    return array[idx]

def try_get_bit(grid,y,x,allelse):
    if y >= len(grid) or y < 0:
        return allelse
    if x >= len(grid[0]) or x < 0:
        return allelse
    return grid[y][x]

def get_neighbor_bits(grid,y,x,allelse):
    bits = []
    bits.append(try_get_bit(grid,y-1,x-1,allelse))
    bits.append(try_get_bit(grid,y-1,x+0,allelse))
    bits.append(try_get_bit(grid,y-1,x+1,allelse))
    bits.append(try_get_bit(grid,y+0,x-1,allelse))
    bits.append(try_get_bit(grid,y+0,x+0,allelse))
    bits.append(try_get_bit(grid,y+0,x+1,allelse))
    bits.append(try_get_bit(grid,y+1,x-1,allelse))
    bits.append(try_get_bit(grid,y+1,x+0,allelse))
    bits.append(try_get_bit(grid,y+1,x+1,allelse))
    return bits

with open("input") as f:
    l = f.readline().strip()
    array = []
    for char in l:
        if char == '.':
            array.append(0)
        elif char == '#':
            array.append(1)
    f.readline() # Eat the blank line
    ngrid = []
    ogrid = []
    for line in f.readlines():
        row = []
        l = line.strip()
        for char in line:
            if char == '.':
                row.append(0)
            elif char == '#':
                row.append(1)
        ngrid.append(row)
    
    iterations = 50
    allelse = 0
    for i in range(iterations):
        # Add new space
        r1, r2 = [allelse]*len(ngrid[0]), [allelse]*len(ngrid[0])
        ngrid.insert(0,r1)
        ngrid.append(r2)
        for row in ngrid:
            row.insert(0,allelse)
            row.append(allelse)
        # Copy to old
        ogrid = ngrid
        ngrid = copy.deepcopy(ngrid)
        # Update new
        for y in range(len(ngrid)):
            for x in range(len(ngrid[0])):
                ninebits = get_neighbor_bits(ogrid,y,x,allelse)
                ngrid[y][x] = get_from_array(array,ninebits)
        allelse = get_from_array(array,[allelse]*9)
        if i == 2-1:
            output_part(ngrid, '1')
        if i == 50-1:
            output_part(ngrid, '2')

input("Enter to exit")