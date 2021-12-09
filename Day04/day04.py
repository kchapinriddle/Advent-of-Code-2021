# Day 04: Giant Squid

# Part 1
# Problem Summary: input file contains bingo calls, boards.
# Determine winning board, then multiply sum of uncalled numbers on that board by final call

def check_winner(boards):
    for board in boards:
        # Check rows
        for row in board:
            if row == ["X","X","X","X","X"]:
                return board
        # Check columns
        for i in range(5):
            if board[0][i] == "X" and board[1][i] == "X" and board[2][i] == "X" and board[3][i] == "X" and board[4][i] == "X":
                return board
    return []

with open("input") as f:
    # Read in list of calls
    calls = f.readline().strip().split(',')
    
    # Read in bingo boards
    boards = []
    while True:
        if f.readline() == "":
            break # Empty line means EOF, otherwise should be "\n"
        board = []
        for i in range(5):
            board.append(f.readline().strip().split())
        boards.append(board)
    
    # Begin marking, using X as "called" marker
    winner = []
    winnum = 0
    for num in calls:
        # Replace
        for board in boards:
            for row in board:
                for i in range(5):
                    if row[i] == num:
                        row[i] = "X"
        
        # Check for victory
        winner = check_winner(boards)
        if winner:
            winnum = num
            break
    
    # Compute sum
    winsum = 0
    print(winner)
    for row in winner:
        for cell in row:
            if cell != "X":
                winsum += int(cell)
    print(str(int(winnum) * winsum))

input("Enter to exit")