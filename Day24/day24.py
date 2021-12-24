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

# This code only used to test an input/state pair and see results
# Most work done in monad_analysis.txt and worksheet.ods
# This was fundamentally a reverse engineering problem, not a coding problem

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
    
    #Part 1 verify z output
    state = ALU("59996912981939")
    #state.registers[3] = 13+26+26
    print(state)
    for line in instructions:
        state.parse_inst(line)
    print(state)
    
    print()
    
    #Part 2 verify z output
    state = ALU("17241911811915")
    #state.registers[3] = 13+26+26
    print(state)
    for line in instructions:
        state.parse_inst(line)
    print(state)
    
    '''#for zstate in range(26):
    for zstate in [11,11+26]:
        for digit in [1,2]:
        #for digit in range(1,10):
            state = ALU(str(digit))
            state.registers[3] = zstate
            for line in instructions:
                state.parse_inst(line)
            #if state.registers[3] == 0:
            #    print("Z, in:",zstate,digit)
            print("Z, in, out:",zstate, digit, state.registers[3])'''

input("Enter to exit")