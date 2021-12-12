# Day 12: Passage Pathing

# Parts 1,2
# Problem Summary: text file holds pairs of strings: "a-b" notation
# Some are capitalized, some aren't
# One is "start", one is "end"
# Part 1: Find all paths from "start" to "end" that pass through
# each non-capitalized node at most once
# Part 2: Now can take ONE non-capitalized node twice, except "start" and "end"

graph = {}
search_paths = []
through_paths = []

# Take the first path in search_paths, pull it from the queue
# Then add all valid paths deriving from it to the queue
def expand_search(part):
    past = search_paths.pop(0)
    # If done, move to done list and go no further
    if past[-1] == "end":
        through_paths.append(past)
        return
    # Otherwise continue and add to queue
    for node in graph[past[-1]]:
        # Add untaken nodes to the possible paths
        if node not in past:
            search_paths.append(past + [node])
        elif node.isupper(): # allowed to retake CAPITAL nodes
            search_paths.append(past + [node])
        elif part == 2 and node != "start" and node != "end":
            allow_new_nonupper = True
            for n in past: # Allowed to take one lowercase node in part 2, once
                if n != "start" and n.islower(): 
                    if past.count(n) > 1: # So block if already did so
                        allow_new_nonupper = False
                        break
            if allow_new_nonupper:
                search_paths.append(past + [node])

with open("input") as f:
    # Read in all pairings, create dict of connections
    for line in f.readlines():
        l = line.strip().split("-")
        # Add to dict if needed
        for node in l:
            if node not in graph:
                graph[node] = set()
        # Connect first to second, then second to first
        graph[l[0]].add(l[1])
        graph[l[1]].add(l[0])
    
    # Use lists of steps to traverse
    search_paths = [["start"]]
    while len(search_paths) != 0:
        expand_search(part = 1)
    print(len(through_paths))
    
    search_paths = [["start"]]
    through_paths = []
    while len(search_paths) != 0:
        expand_search(part = 2)
    print(len(through_paths))
    

input("Enter to exit")