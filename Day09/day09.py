# Day 09: Smoke Basin

import statistics

# Part 1
# Problem Summary: Given a rectangular grid of single-digit ints,
# find all points where all four cardinal neighbors are edges or larger numbers
# Then for those points, output sum(1+value)
# Part 2
# Problem Summary: Each low point forms a "basin", bordered by 9s or edges
# "Basin" includes all non-9 digits touching, recursively, etc
# "Basin"s will never overlap
# Find the size of the three largest "basin"s, return their product
    
def is_lower(grid, cell, neighbor, bounds):
    if neighbor[0] >= bounds[0] or neighbor[1] >= bounds[1] or neighbor[0] < 0 or neighbor[1] < 0:
        return True #Out of bounds check
    return grid[cell[0]][cell[1]] < grid[neighbor[0]][neighbor[1]]

def num_lower(grid, cell, bounds):
    neighbors = [(cell[0]+1,cell[1]),(cell[0],cell[1]+1),(cell[0]-1,cell[1]),(cell[0],cell[1]-1)]
    lower = 0
    for n in neighbors:
        if is_lower(grid,cell,n,bounds):
            lower += 1
    return lower

def is_risk_zone(grid, cell, bounds):
    if num_lower(grid,cell,bounds) == 4:
        return 1
    return 0

def spread_basin(basingrid, risk, bounds):
    index = basingrid[risk[0]][risk[1]]
    processed = set()
    to_process = {risk}
    while to_process != set():
        c = to_process.pop()
        if c[0] < 0 or c[1] < 0 or c[0] >= bounds[0] or c[1] >= bounds[1]:
            processed.add(c)
            continue #Out of bounds, ignore
        if basingrid[c[0]][c[1]] == ' ':
            processed.add(c)
            continue #9, ignore
        else:
            basingrid[c[0]][c[1]] = index # Set as part of basin
            add = {(c[0],c[1]+1),(c[0],c[1]-1),(c[0]+1,c[1]),(c[0]-1,c[1])}
            add = add - processed
            to_process = to_process | add # Add neighbors to list unless they've been tried
            processed.add(c) # Mark this as done
    return basingrid
            
            

with open("input") as f:
    risk_count = 0
    
    # Read in grid
    grid = []
    for line in f.readlines():
        line = line.strip()
        row = []
        for digit in line:
            row.append(int(digit))
        grid.append(row)
    
    # Identify risk zones
    bounds = len(grid),len(grid[0])
    riskgrid = []
    for i in range(bounds[0]):
        row = []
        for j in range(bounds[1]):
            cell = (i,j)
            row.append(is_risk_zone(grid, cell, bounds))
        riskgrid.append(row)
    
    # Sum and output
    total = 0
    for i in range(bounds[0]):
        for j in range(bounds[1]):
            risk_count += riskgrid[i][j]
            total += riskgrid[i][j]*(1+grid[i][j])
    print("P1: Sum of risk levels is " + str(total))
    
    # Set up basin grid
    basingrid = []
    risk_index = 0
    risk_coords = []
    for i in range(bounds[0]):
        row = []
        for j in range(bounds[1]):
            if riskgrid[i][j] == 1: #New basin start
                row.append(risk_index)
                risk_coords.append((i,j))
                risk_index += 1
            elif grid[i][j] == 9:
                row.append(" ")
            else:
                row.append("?")
        basingrid.append(row)
    
    # Spread basins
    for i in range(risk_index):
        basingrid = spread_basin(basingrid,risk_coords[i],bounds)
    
    # Get sizes
    # Could have been done in spread_basin without this extra pass,
    # but this doesn't increase the time complexity
    basin_size_list = []
    for r in range(risk_index):
        basin_size = 0
        for i in range(bounds[0]):
            for j in range(bounds[1]):
                if basingrid[i][j] == r:
                    basin_size += 1
        basin_size_list.append(basin_size)
    
    # Sort, output
    basin_size_list.sort(reverse = True)
    print("P2: Product of three largest basins: " +str(basin_size_list[0]*basin_size_list[1]*basin_size_list[2]))


input("Enter to exit")