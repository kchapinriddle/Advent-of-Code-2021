# Day 05: Hydrothermal Venture

# Part 1
# Problem Summary: Input file has pairs of ordered pairs, which are coordinates in 2-space. 
# Where coordinates form horizontal/vertical line segments, increment field values along that segment
# Return number of points with value >= 2

with open("input") as f:
    # Parse lists of pairs, only keep h/v lines
    lines = f.readlines()
    pairs = []
    for line in lines:
        line = line.strip().split(" -> ")
        pair = line[0].split(",") + line[1].split(",")
        pair = list(map(int,pair))
        if pair[0] == pair[2] or pair[1] == pair[3]:
            pairs.append(pair)
    
    # Set up the field
    maxX = 0
    maxY = 0
    for p in pairs:
        maxX = max(maxX, p[0], p[2])
        maxY = max(maxY, p[1], p[3])
    field = [[0]*(maxX+1) for _ in range(maxY+1)]
    
    # Increment line segments
    for p in pairs:
        if p[0] == p[2]: # Horizontal segment
            Y = p[0]
            for X in range(min(p[1],p[3]), max(p[1],p[3])+1): #+1 due to range removing highest
                field[X][Y] += 1
        elif p[1] == p[3]: # Horizontal segment
            X = p[1]
            for Y in range(min(p[0],p[2]), max(p[0],p[2])+1): #+1 due to range removing highest
                field[X][Y] += 1
    
    # Count values > 1
    overlaps = 0
    for row in field:
        for point in row:
            if point > 1:
                overlaps += 1
    
    print("P1 Overlaps: " + str(overlaps))

# Part 2
# Now also consider 45 degree lines

with open("input") as f:
    # Parse lists of pairs, only keep h/v lines
    lines = f.readlines()
    pairs = []
    diag_pairs = []
    for line in lines:
        line = line.strip().split(" -> ")
        pair = line[0].split(",") + line[1].split(",")
        pair = list(map(int,pair))
        if pair[0] == pair[2] or pair[1] == pair[3]:
            pairs.append(pair)
        elif abs(pair[0] - pair[2]) == abs(pair[1] - pair[3]):
            diag_pairs.append(pair)
    
    # Set up the field
    maxX = 0
    maxY = 0
    for p in pairs:
        maxX = max(maxX, p[0], p[2])
        maxY = max(maxY, p[1], p[3])
    for p in diag_pairs:
        maxX = max(maxX, p[0], p[2])
        maxY = max(maxY, p[1], p[3])
    field = [[0]*(maxX+1) for _ in range(maxY+1)]
    
    # Increment line segments
    for p in pairs:
        if p[0] == p[2]: # Horizontal segment
            Y = p[0]
            for X in range(min(p[1],p[3]), max(p[1],p[3])+1): #+1 due to range removing highest
                field[X][Y] += 1
        elif p[1] == p[3]: # Horizontal segment
            X = p[1]
            for Y in range(min(p[0],p[2]), max(p[0],p[2])+1): #+1 due to range removing highest
                field[X][Y] += 1
    
    # Now the diagonals
    for dp in diag_pairs:
        Y = dp[0]
        X = dp[1]
        dY = int(abs(dp[2]-Y)/(dp[2]-Y))
        dX = int(abs(dp[3]-X)/(dp[3]-X))
        while Y != dp[2]:
            field[X][Y] += 1
            X += dX
            Y += dY
        field[X][Y] += 1 # Get that last point!
    
    # Count values > 1
    overlaps = 0
    for row in field:
        for point in row:
            if point > 1:
                overlaps += 1
    
    print("P2 Overlaps: " + str(overlaps))

input("Enter to exit")