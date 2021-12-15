# Day 15: Chiton

# Parts 1,2
# Problem Summary: Input is grid of single-digit ints
# Find path from top left to bottom right, minimizing sum of cells traversed
# Starting cell *does not count*
# Part 1: Print sum of cells on "shortest" route
# Part 2: Copy/paste grid into 5x5 equivalent, each copy down or right having
# value +1 for each cell, 10+ wrapping around to 1
# Print sum of cells on "shortest" route for this supergrid

verybignum = 999999

class Cell:
    def __init__(self, x, y, risk, sumrisk = verybignum):
        self.x = x
        self.y = y
        self.risk = risk
        self.sumrisk = sumrisk

def find_sumrisk_neighbors(cell, grid, unvisited):
    x = cell.x
    y = cell.y
    for c in [[x,y-1],[x-1,y],[x,y+1],[x+1,y]]:
        if c[0] < 0 or c[1] < 0 or c[1] >= len(grid) or c[0] >= len(grid[0]):
            continue
        comp = grid[c[1]][c[0]]
        if comp.sumrisk == verybignum:
            unvisited.add(comp)
        comp.sumrisk = min(cell.sumrisk + comp.risk, comp.sumrisk)

def print_riskgrid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            print(grid[y][x].risk, end='')
        print()
    print()

def traverse_grid(g,part):
    # Properly set first cell
    current = g[0][0]
    current.sumrisk = 0
    # Set up list of cells to visit
    unvisited = {current}
    # Destination!
    destination = g[len(g)-1][len(g[0])-1]
    # Traverse
    while True:
        find_sumrisk_neighbors(current,g,unvisited)
        unvisited.remove(current)
        minrisk = verybignum
        # Find next cell based on lowest sum risk to get there
        for c in unvisited:
            if c.sumrisk != verybignum and c.sumrisk < minrisk:
                minrisk = c.sumrisk
                current = c
        if current == destination: 
            print("Part "+ part +": " + str(current.sumrisk))
            break
        if minrisk == verybignum:
            print("No path! Aborting!")
            break


with open("input") as f:
    # Set up grid
    grid = []
    supergrid = []
    y = 0
    for line in f.readlines():
        x = 0
        l = line.strip()
        row = []
        for i in l:
            c = Cell(x,y,int(i))
            row.append(c)
            x += 1
        grid.append(row)
        # Copy across for 5x5 supergrid
        superrow = row.copy()
        for x in range(len(superrow)):
            superrow[x] = Cell(row[x].x,row[x].y,row[x].risk)
        for i in range(1,5):
            # Copy cells
            nrow = []
            for i in row:
                nrow.append(Cell(i.x,i.y,i.risk))
            row = nrow
            for j in range(len(row)):
                row[j].risk += 1
                if row[j].risk == 10:
                    row[j].risk = 1
                row[j].x += len(row)
            superrow += row
        supergrid.append(superrow)
        y += 1

    # Copy down for 5x5 supergrid
    for i in range(1,5):
        # Copy first rows for template
        supergridrows = []
        for j in range(len(grid)):
            row = []
            for k in range(len(supergrid[0])):
                row.append(supergrid[j][k])
            supergridrows.append(row)
        # Copy the rows
        for j in range(len(supergridrows)):
            for k in range(len(supergridrows[0])):
                c = supergridrows[j][k]
                supergridrows[j][k] = Cell(c.x,c.y,c.risk)
                supergridrows[j][k].y += i*len(grid)
                supergridrows[j][k].risk += i
                if supergridrows[j][k].risk >= 10:
                    supergridrows[j][k].risk -= 9
        supergrid += supergridrows.copy()
    
    traverse_grid(grid,"1")
    traverse_grid(supergrid,"2")

input("Enter to exit")