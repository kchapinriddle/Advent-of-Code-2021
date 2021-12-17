# Day 17: Trick Shot

# Parts 1,2
# Problem Summary: Read in a target area from file
# Then compute ballistic trajectories - each step of computation, 
# x += x', y += y', abs(x')--, y'--
# To hit, a shot must be in the target area _on a step_, skipping over doesn't count
# Part 1: Find highest point reachable by shot that passes through target area
# Part 2: Find number of valid trajectories

with open("input") as f:
    # Get target area
    line = f.readline().strip().split(", y=")
    miny, maxy = int(line[1].split("..")[0]), int(line[1].split("..")[1])
    maxx = int(line[0].split("..")[1])
    minx = int(line[0].split("..")[0].split("=")[1])
    # Key trick(?): If initial y velocity > 0, shot will return to y=0 with velocity (-initial -1)
    vx, vy = -1, -1
    vy = -1 * miny - 1
    i = 0
    while True:
        if i*(i+1)/2 >= minx and i*(i+1)/2 <= maxx:
            vx = i
            break
        if i*(i+1)/2 > maxx:
            break
        i += 1
    # Now, for part 1, compute greatest height reached
    greatesty = int(vy*(vy+1)/2)
    print("vx vy:", vx, vy)
    print("Part1:", greatesty)
    
    # Actually, let's compute *all* valid values
    shots = []
    for vx in range(maxx+2):
        for vy in range(miny,-1*miny +1):
            x, y = 0, 0
            dx, dy = vx, vy
            cont = True
            while cont:
                x += dx
                y += dy
                dx = max(0, dx-1)
                dy -= 1
                if x >= minx and y >= miny and x <= maxx and y <= maxy:
                    if not [vx,vy] in shots:
                        shots.append([vx,vy])
                    cont = False
                if x > maxx or y < miny:
                    cont = False
    print("Part 2:", len(shots))

input("Enter to exit")