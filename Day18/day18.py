# Day 18: Snailfish

# Parts 1,2
# Problem Summary: 
# Defies easy summary. See problem statements.

import copy

# TESTED init
# TESTED magnitude
# TESTED explode_check
# TESTED split_check
# TESTED reduce
# TESTED explode
# TESTED split
# TESTED addition
# DONE finish up

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
    
    def copy(self):
        cpy = sfnum(None, [0,0])
        if type(self.left) == int:
            cpy.left = self.left
        else:
            cpy.left = self.left.copy()
            cpy.left.parent = cpy
        if type(self.right) == int:
            cpy.right = self.right
        else:
            cpy.right = self.right.copy()
            cpy.right.parent = cpy
        return cpy
    
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
    
    def explode_down(self,number,direction):
        #print("D_XD",direction,self)
        if direction == "L":
            if type(self.right) == int:
                self.right += number
            else:
                self.right.explode_down(number,direction)
        elif direction == "R":
            if type(self.left) == int:
                self.left += number
            else:
                self.left.explode_down(number,direction)
    
    def explode_up(self,number,direction):
        #print("D_XU",direction,self)
        if self.parent == None: # Reached the top, done
            return
        elif (direction == "L" and self.parent.left == self) or (direction == "R" and self.parent.right == self):
            self.parent.explode_up(number,direction)
        elif direction == "L":
            if type(self.parent.left) == int:
                self.parent.left += number
            else:
                self.parent.left.explode_down(number,direction)
        elif direction == "R":
            if type(self.parent.right) == int:
                self.parent.right += number
            else:
                self.parent.right.explode_down(number,direction)
    
    def explode(self):
        #print("D_XX",self)
        assert type(self.left == int)
        assert type(self.right == int)
        self.explode_up(self.left,"L")
        self.explode_up(self.right,"R")
        if self.parent.left == self:
            self.parent.left = 0
        elif self.parent.right == self:
            self.parent.right = 0
    
    def explode_check(self, depth = 0):
        if depth == 4:
            self.explode()
            return True
        else:
            if type(self.left) != int and self.left.explode_check(depth+1):
                return True
            elif type(self.right) != int and self.right.explode_check(depth+1):
                return True
        return False
    
    def split(self):
        if type(self.left) == int:
            if self.left >= 10:
                self.left = sfnum(self,[self.left//2,-(-self.left//2)])
                return
        if type(self.right) == int:
            if self.right >= 10:
                self.right = sfnum(self,[self.right//2,-(-self.right//2)])
                return
    
    def split_check(self):
        if type(self.left) == int and self.left >= 10:
            self.split()
            return True
        elif type(self.left) != int and self.left.split_check():
            return True
        elif type(self.right) == int and self.right >= 10:
            self.split()
            return True
        elif type(self.right) != int and self.right.split_check():
            return True
        return False
    
    def reduce(self):
        while True:
            if self.explode_check():
                continue
            elif self.split_check():
                continue
            else:
                return

def add_sfnums(left, right):
    new_sfnum = sfnum(None, [0,0])
    new_sfnum.left = left.copy()
    new_sfnum.left.parent = new_sfnum
    new_sfnum.right = right.copy()
    new_sfnum.right.parent = new_sfnum
    new_sfnum.reduce()
    return new_sfnum

with open("input") as f:
    numbers = []
    for line in f.readlines():
        l = line.strip()
        for char in l:
            if not char in "[],1234567890":
                print("Unexpected character found, aborting before eval")
                exit()
        n = eval(l) # Normally very unsafe to do, but very easy
        sfn = sfnum(None, n)
        sfn.reduce()
        numbers.append(sfn)
    sfnumsum = numbers[0]
    for n in range(1,len(numbers)):
        sfnumsum = add_sfnums(sfnumsum, numbers[n])
    print("Part 1:",sfnumsum.magnitude())
    maxsum = 0
    for i in numbers:
        for j in numbers:
            if i == j:
                continue
            maxsum = max(maxsum, add_sfnums(i,j).magnitude())
    print("Part 2:",maxsum)

input("Enter to exit")