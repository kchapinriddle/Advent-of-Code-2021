# Day 06: Lanternfish

# Part 1
# Problem Summary: Exponentially growing fish, with individual initial timers read from input file
# On 'tick': Timers above 0 decrement. Timer 0 fish reset to timer 6, create a timer 8 fish
# Run until day 80
# Part 2: Run until day 256

with open("input") as f:
    infish = f.read()
    fish = []
    for i in range(9):
        fish.append(infish.count(str(i)))
    day = 0
    while day < 256:
        newfish = [0]*9
        for i in range(1,9): # Fish not age 0 move toward reproduction
            newfish[i-1] = fish[i]
        newfish[6] += fish[0]
        newfish[8] += fish[0]
        fish = newfish
        
        day += 1
        if day == 80:
            print(fish)
            print(str(sum(fish)))
        if day == 256:
            print(fish)
            print(str(sum(fish)))

input("Enter to exit")