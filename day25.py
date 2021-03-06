import sys
import itertools

class Program:
    cur_pc = 0
    relative_base = 0
    output = []
    input = []
    input_function = None
    halt = False
    def __init__(self, codes, input, input_function, output_function):
        self.codes = codes.copy()
        self.input = input.copy()
        self.input_function = input_function
        self.output_function = output_function
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
            #print(instruction)
            modes[2] = int(instruction[-5:-4])

        if opcode == 99:
            #print("BREAK")
            self.halt = True
        #print("MODES = " + str(modes))
        if opcode == 1 or opcode == 2 or opcode == 4 or opcode == 5 or opcode == 6 or opcode == 7 or opcode == 8 or opcode == 9:
            if modes[0] == 0:
                a = self.codes[self.codes[pc+1]]
            elif modes[0] == 2:
                a = self.codes[self.relative_base + self.codes[pc+1]]
            else:
                a = self.codes[pc+1]
        if opcode == 1 or opcode == 2 or opcode == 5 or opcode == 6 or opcode == 7 or opcode == 8:
            if modes[1] == 0:
                b = self.codes[self.codes[pc+2]]
            elif modes[1] == 2:
                b = self.codes[self.relative_base + self.codes[pc+2]]
            else:
                b = self.codes[pc+2]
        three_dest_addr = self.codes[pc+3]
        two_dest_addr = self.codes[pc+2]
        if modes[2] == 2:
            three_dest_addr += self.relative_base
            two_dest_addr += self.relative_base
        if opcode == 1:
            #print(str(pc) + " " + instruction + " ADD " + str(a) + " " + str(b) + "->" + str(codes[pc+3]))
            self.codes[three_dest_addr] = a + b
            pc += 4
        elif opcode == 2:
            #print(str(pc) + " " + instruction + " MULTIPLY " + str(a) + " " + str(b) + "->" + str(codes[pc+3]))
            self.codes[three_dest_addr] = a * b
            pc += 4
        elif opcode == 3:
            if self.input_function:
                if len(self.input) > 0:
                    value = self.input.pop(0)
                else:
                    value = self.input_function()
            else:
                if len(self.input) == 0:
                    self.waiting = True
                    return None
                else:
                    self.waiting = False
                value = self.input.pop(0)
            #if value != -1: print("INPUT: " + str(value))
            #print(str(pc) + " " + instruction + " STORE " + str(value) + " @ " + str(self.codes[pc+1]))
            if modes[0] == 2:
                self.codes[self.relative_base + self.codes[pc+1]] = value
            else:
                self.codes[self.codes[pc+1]] = value
            pc += 2
        elif opcode == 4:
            self.output.append(a)
            new_output = a
            if self.output_function:
                self.output_function(a)
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
            self.codes[three_dest_addr] = 1 if a < b else 0
            pc += 4
        elif opcode == 8: # equals
            self.codes[three_dest_addr] = 1 if a == b else 0
            pc += 4
        elif opcode == 9: # set relative base
            self.relative_base += a
            pc += 2
        elif opcode != 99:
            print("Illegal Opcode " + instruction)
            self.halt = True
        self.cur_pc = pc
        return new_output

input_buffer = []
def on_input():
    global input_buffer
    if len(input_buffer) > 0:
        input = input_buffer.pop(0)
        return input
    else:
        return -1

output_buffer = []
def on_output(output):
    global output_buffer, packet_queue, nat_packet
    if output == 10:
        print(''.join(output_buffer))
        output_buffer = []
    else:
        output_buffer.append(chr(output))
        #print("OUTPUT " + str(output))


codes = []
with open('day25.txt') as file:
    for line in file:
        codes.extend(line.rstrip().split(","))

int_codes = list(map(lambda x: int(x), codes))
int_codes.extend([0] * 10000)

program = Program(int_codes, [], None, on_output)

items = ['ornament', 'klein bottle', 'dark matter', 'candy cane', 'hologram', 'astrolabe', 'whirled peas', 'tambourine']
def try_all_combinations():
    attempts = []
    for i in range(1, len(items)):
        attempts.extend(itertools.combinations(items, i))
    output = []
    for attempt in attempts:
        for item in attempt:
            output.append("take " + item + "\n")
        output.append("north\n")
        for item in attempt:
            output.append("drop " + item + "\n")
    return ''.join(output)


steps = 0
while True:
    while not program.waiting:
        #print("program run")
        program.step()
        steps += 1
        if program.halt:
            print("HALT")
            break
    input_line = input("[> ")
    if input_line.startswith("perm"):
        input_line = try_all_combinations()
    program.input.extend(list(map(ord, input_line)))
    program.input.append(10)
    program.waiting = False

    
    