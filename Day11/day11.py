# Day 11: Dumbo Octopus

# Parts 1,2
# Problem Summary: 10x10 grid of ints
# Each step, increment everything in grid,
# then everything > 9 increments all neighbors,
# then everything > 9 = 0
# Part 1: Determine how many elements reached > 9 total after step 100
# Part 2: Determine which step all elements reach > 9 on

flashes = 0
flashes_this_step = 0

# Just prints it all nice and pretty
def printgrid(grid):
    for y in range(10):
        for x in range(10):
            print(grid[y][x], end='')
        print()
    print()

# Increment target cell if not 0
def try_increase_energy(grid, x, y):
    if grid[y][x] == 0:
        return
    else:
        grid[y][x] += 1

# Set cell to 0, increment non-0 neighbors
def flash(grid, x, y):
    global flashes
    global flashes_this_step
    flashes += 1
    flashes_this_step += 1
    returnval = set()
    grid[y][x] = 0
    for i in range(-1,2):
        for j in range(-1,2):
            xx = x + i
            yy = y + j
            if xx in range(10) and yy in range(10): 
                try_increase_energy(grid, xx, yy)
                if grid[yy][xx] > 9:
                    returnval.add((yy,xx))
    return returnval
        

with open("input") as f:
    # Read in grid of octopi
    grid = []
    for line in f.readlines():
        l = list(map(int,line.strip()))
        grid.append(l)
    
    step = 0
    while True:
        flashes_this_step = 0
        # First, increment energy of all octopi
        for y in range(10):
            for x in range(10):
                grid[y][x] += 1
        # Then all octopi > 9 flash, increasing nearby energy levels
        to_increment = set()
        for y in range(10):
            for x in range(10):
                if grid[y][x] > 9:
                    to_increment.add((y,x))
        while to_increment != set():
            c = to_increment.pop()
            to_increment = to_increment | flash(grid, c[1], c[0])
        # Move towards completion
        step += 1
        if step == 100:
            print("P1: " + str(flashes))
        if flashes_this_step == 100:
            print("P2: " + str(step))
            break

input("Enter to exit")