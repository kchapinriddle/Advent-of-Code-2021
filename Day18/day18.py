# Day 18: Snailfish

# Parts 1,2
# Problem Summary: 
# Defies easy summary. See problem statements.

# TESTED init
# TESTED magnitude
# TESTEDish explode_check
# TESTEDish split_check
# TODO TEST reduce
# TODO explode
# TODO split
# TODO addition
# TODO finish up

class sfnum:
    def __init__(self, parent, data):
        self.parent = parent
        if type(data[0]) == int:
            self.left = data[0]
        else:
            self.left = sfnum(self, data[0])
        if type(data[1]) == int:
            self.right = data[1]
        else:
            self.right = sfnum(self, data[1])
    def __str__(self):
        return "["+str(self.left)+","+str(self.right)+"]"
    
    def magnitude(self):
        val = 0
        if type(self.left) == int:
            val += 3 * self.left
        else:
            val += 3 * self.left.magnitude()
        if type(self.right) == int:
            val += 2 * self.right
        else:
            val += 2 * self.right.magnitude()
        return val
    
    def explode_check(self, depth = 0):
        if depth == 4:
            print(self)
            # TODO: explode call goes here
            return True
        else:
            if type(self.left) == int:
                pass
            elif self.left.explode_check(depth+1):
                return True
            elif type(self.right) == int:
                return False
            elif self.right.explode_check(depth+1):
                return True
        return False
    
    def split_check(self):
        if type(self.left) == int:
            if self.left >= 10:
                # TODO: split call goes here
                print(self, self.left)
                return True
        elif self.left.split_check():
            return True
        elif type(self.right) == int:
            if self.right >= 10:
                # TODO: split call goes here
                print(self, self.right)
                return True
        elif self.right.split_check():
            return True
        return False
    
    def reduce(self):
        while True:
            if self.explode_check():
                continue
            if self.split_check():
                continue

with open("input") as f:
    numbers = []
    for line in f.readlines():
        n = eval(line.strip()) # Normally very unsafe to do, but very easy
        sfn = sfnum(None, n)
        print(sfn)

input("Enter to exit")