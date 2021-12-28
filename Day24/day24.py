# Day 24: Arithmetic Logic Unit

# Parts 1,2
# Problem Summary: 
# Four registers (integer variables): w x y z. 
# Six instructions, a is always a variable, b can be a variable or int literal:
# inp a - read input value, store in a
# add a b - add a to b, store in a: a += b
# mul a b - multiply a by b, store in a: a *= b
# div a b - divide a by b, round towards 0, store in a: a //= b
    # b != 0
# mod a b - take a modulo b, store in a: a %= b
    # a >= 0, b > 0
# eql a b - if a == b, store 1 in a else store 0 in a: a = a==b

# Part 1:
# Real program input: ALU program "MONAD" containing exactly 14 inp commands
# Provide a single non-zero digit to each, then check final state of register z
# Find largest 14-digit string that results in z == 0

# Part 2: Find smallest 14-digit string that results in z == 0

# This code (WAS) only used to test an input/state pair and see results
# Most work done in monad_analysis.txt and worksheet.ods
# This was fundamentally a reverse engineering problem, not a coding problem
# NOT ANYMORE, now derives the correct input strings from the program

reg_ids = {'w':0, 'x':1, 'y':2, 'z':3}

class ALU:
    def __init__(self, inputstring):
        self.inputstring = list(inputstring[::-1]) # Flip it backwards so pop() works
        self.registers = [0,0,0,0]
    
    def get_val(self, thing):
        if thing in "wxyz":
            return self.registers[reg_ids[thing]]
        else:
            return int(thing)
    
    def __str__(self):
        return str(self.registers) + str(self.inputstring)
    
    def do_inp(self, ops):
        self.registers[reg_ids[ops[0]]] = int(self.inputstring.pop())
    
    def do_add(self, ops):
        a, b = reg_ids[ops[0]], ops[1]
        self.registers[a] += b
    
    def do_mul(self, ops):
        a, b = reg_ids[ops[0]], ops[1]
        self.registers[a] *= b
    
    def do_div(self, ops):
        a, b = reg_ids[ops[0]], ops[1]
        self.registers[a] = int(self.registers[a] / b)
    
    def do_mod(self, ops):
        a, b = reg_ids[ops[0]], ops[1]
        self.registers[a] = self.registers[a] % b
    
    def do_eql(self, ops):
        a, b = reg_ids[ops[0]], ops[1]
        if self.registers[a] == b:
            self.registers[a] = 1
        else:
            self.registers[a] = 0
    
    def parse_inst(self, inst):
        if inst == "":
            return
        ops = inst.split(' ')
        ops.pop(0)
        if len(ops) > 1:
            ops[1] = self.get_val(ops[1])
        if inst[0] == 'i':
            self.do_inp(ops)
        elif inst[0] == 'a':
            self.do_add(ops)
        elif inst[0] == 'm' and inst[1] == 'u':
            self.do_mul(ops)
        elif inst[0] == 'd':
            self.do_div(ops)
        elif inst[0] == 'm' and inst[1] == 'o':
            self.do_mod(ops)
        elif inst[0] == 'e':
            self.do_eql(ops)
        else:
            print("Error: Instruction matched no known command!")

with open("input") as f:
    # Read in the program
    instructions = []
    for line in f.readlines():
        instructions.append(line.strip())
    
    # Break the program into blocks, identify push and pop blocks and their constants
    block = [] # Entries are [line 5 constant, line 6 constant, line 16 constant]
    stack_constants = [] # Entries are [push constant, push index]
    stack_pairs = [] # Entries are [push constant, pop constant, push index, pop index]
    for i in range(len(instructions)):
        if i % 18 == 5-1: # Record indicator of push or pop behavior: 1 means push, 26 means pop
            block.append(int(instructions[i].split(' ')[2]))
        elif i % 18 == 6-1: # Record constant for pop-type block: pushes (this+input)
            block.append(int(instructions[i].split(' ')[2]))
        elif i % 18 == 16-1: # Record constant for push-type block: pops iff top is (this+input)
            block.append(int(instructions[i].split(' ')[2]))
        elif i % 18 == 18-1: # End of block, handle it
            if block[0] == 1:
                stack_constants.append([block[2],int(i/18)])
            elif block[0] == 26:
                stack_pairs.append([stack_constants[-1][0],block[1],stack_constants[-1][1],int(i/18)])
                stack_constants.pop()
            block = [] # And reset for the next block
    
    # Use identified paired blocks to construct largest and smallest inputs
    max_inl, min_inl = [0]*14, [0]*14
    for sp in stack_pairs:
        difference = sp[0] + sp[1] # push input - pop input must equal this
        ip = [0,0,0,0] # max then min
        if difference >= 0:
            ip[0],ip[1] = 9-difference, 9
            ip[2],ip[3] = 1, 1+difference
        elif difference < 0:
            ip[0],ip[1] = 9, 9+difference
            ip[2],ip[3] = 1-difference, 1
        max_inl[sp[2]],max_inl[sp[3]] = ip[0],ip[1]
        min_inl[sp[2]],min_inl[sp[3]] = ip[2],ip[3]

    max_in = ""
    for c in max_inl:
        max_in += str(c)
    min_in = ""
    for c in min_inl:
        min_in += str(c)
    
    #Part 1 verify z output
    #state = ALU("59996912981939")
    state = ALU(max_in)
    
    for line in instructions:
        state.parse_inst(line)
    print("Part 1: Derived input is", max_in, "value of z was", state.registers[3], "(should be 0)")
    
    #Part 2 verify z output
    #state = ALU("17241911811915")
    state = ALU(min_in)
    for line in instructions:
        state.parse_inst(line)
    print("Part 2: Derived input is", min_in, "value of z was", state.registers[3], "(should be 0)")

input("Enter to exit")