# Day 1: Dive!

# Part 1
# Problem summary: Given a file containing one command per line,
# where each command is a direction and an int separated by a space,
# track the position and output depth*horizontal distance
depth = 0
horizontal = 0
with open("input") as f:
    for line in f:
        command = line.strip().split(' ')
        if command[0] == "forward":
            horizontal += int(command[1])
        elif command[0] == "down":
            depth += int(command[1])
        elif command[0] == "up":
            depth -= int(command[1])
    print("Depth: " + str(depth))
    print("Horizontal: " + str(horizontal))
    print("Product: " + str(depth*horizontal))

# Part 2
# Problem summary: Given a file containing one command per line,
# where each command is a direction and an int separated by a space,
# track the position and output depth*horizontal distance
# However, "up" and "down" alter a multiplier instead of depth
# the multiplier modifies depth based on "forward" commands
depth = 0
horizontal = 0
aim = 0
with open("input") as f:
    for line in f:
        command = line.strip().split(' ')
        if command[0] == "forward":
            horizontal += int(command[1])
            depth += aim * int(command[1])
        elif command[0] == "down":
            aim += int(command[1])
        elif command[0] == "up":
            aim -= int(command[1])
    print("Depth: " + str(depth))
    print("Horizontal: " + str(horizontal))
    print("Product: " + str(depth*horizontal))

input("Enter to exit")