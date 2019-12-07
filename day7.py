from itertools import permutations 

class Program:
    cur_pc = 0
    output = []
    input = []
    halt = False
    def __init__(self, codes, input):
        self.codes = codes.copy()
        self.input = input.copy()
        self.cur_pc = 0
        self.output = []
        self.halt = False
        self.waiting = False

    def step(self):
        new_output = None
        pc = self.cur_pc
        instruction = str(self.codes[pc])
        #print("INS " + instruction)
        opcode = int(instruction[-2:])
        #print(str(pc) + " Opcode: " + str(opcode))
        modes = [0,0,0]

        if len(instruction) > 2:
            modes[0] = int(instruction[-3:-2])
        if len(instruction) > 3:
            modes[1] = int(instruction[-4:-3])
        if len(instruction) > 4:
            modes[2] = int(instruction[-5:-4])

        if opcode == 99:
            #print("BREAK")
            self.halt = True
        #print("MODES = " + str(modes))
        if opcode == 1 or opcode == 2 or opcode == 4 or opcode == 5 or opcode == 6 or opcode == 7 or opcode == 8:
            if modes[0] == 0:
                a = self.codes[self.codes[pc+1]]
            else:
                a = self.codes[pc+1]
        if opcode == 1 or opcode == 2 or opcode == 5 or opcode == 6 or opcode == 7 or opcode == 8:
            if modes[1] == 0:
                b = self.codes[self.codes[pc+2]]
            else:
                b = self.codes[pc+2]
        if opcode == 1:
            #print(str(pc) + " " + instruction + " ADD " + str(a) + " " + str(b) + "->" + str(codes[pc+3]))
            self.codes[self.codes[pc+3]] = a + b
            pc += 4
        elif opcode == 2:
            #print(str(pc) + " " + instruction + " MULTIPLY " + str(a) + " " + str(b) + "->" + str(codes[pc+3]))
            self.codes[self.codes[pc+3]] = a * b
            pc += 4
        elif opcode == 3:
            if len(self.input) == 0:
                self.waiting = True
                return None
            else:
                self.waiting = False
            value = self.input.pop(0)
            #print(str(pc) + " " + instruction + " STORE " + str(value) + " @ " + str(self.codes[pc+1]))
            self.codes[self.codes[pc+1]] = value
            pc += 2
        elif opcode == 4:
            self.output.append(a)
            new_output = a
            #print(str(pc) + " " + instruction + " OUTPUT " + str(new_output))
            pc += 2
        elif opcode == 5: # jump-if-true
            if a != 0:
                pc = b
            else:
                pc += 3
        elif opcode == 6: # jump-if-false
            if a == 0:
                pc = b
            else:
                pc += 3
        elif opcode == 7: # less then
            self.codes[self.codes[pc+3]] = 1 if a < b else 0
            pc += 4
        elif opcode == 8: # equals
            self.codes[self.codes[pc+3]] = 1 if a == b else 0
            pc += 4
        self.cur_pc = pc
        return new_output

def run_program(codes, input):
    prog = Program(codes, input)
    while True:
        prog.step()
        if prog.halt:
            break
    return prog.output

def run_sequence(code, sequence):
    prev_output = [0]
    for seq in sequence:
        prev_output = run_program(code.copy(), [seq, prev_output[0]])
    return prev_output[0]

example1 = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"   
example2 = "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"   
part2_example = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"
part2_example2 = "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"
#codes = part2_example.split(',')
codes = []
with open('day7.txt') as file:
    for line in file:
        codes.extend(line.split(','))
int_codes = list(map(lambda x: int(x), codes))

part1 = True
part2 = True
if part1:
    best = 0
    best_seq = []
    perm = permutations([4, 3, 2, 1, 0])
    for i in list(perm):
        print(i)
        result = run_sequence(int_codes.copy(), i)
        print(result)
        if result > best:
            best = result
            best_seq = i
    print("Part1 Best Perm " + str(best_seq))
    print("Part1 Best: "+ str(best))

if part2:
    best = 0
    best_seq = []
    perm = permutations([9, 8, 7, 6, 5])
    for p in perm:
        progs = []
        progs.append(Program(int_codes.copy(), [p[0], 0]))
        progs.append(Program(int_codes.copy(), [p[1]]))
        progs.append(Program(int_codes.copy(), [p[2]]))
        progs.append(Program(int_codes.copy(), [p[3]]))
        progs.append(Program(int_codes.copy(), [p[4]]))
        any_running = True
        while any_running:
            any_running = False
            for i in range(0, len(progs)):
                if not progs[i].halt:
                    any_running |= (not progs[i].waiting) or len(progs[i].input) > 0
                    new_output = progs[i].step()
                    if new_output:
                        if (i+1) < len(progs):
                            #print("Append " + str(new_output) + " to " + str(i+1))
                            progs[i+1].input.append(new_output)
                        else:
                            #print("Append " + str(new_output) + " to " + str(0))
                            progs[0].input.append(new_output)
        if len(progs[4].output) > 0:
            result = progs[4].output[-1]
            if result > best:
                best = result
                best_seq = p
    print("Part2 Best Perm " + str(best_seq))
    print("Part2 Best: "+ str(best))


