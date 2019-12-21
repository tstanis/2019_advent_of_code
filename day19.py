import copy

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
                value = self.input_function()
            else:
                if len(self.input) == 0:
                    self.waiting = True
                    return None
                else:
                    self.waiting = False
                value = self.input.pop(0)
                #print("INPUT: " + str(value))
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

count_points = 0
cursor = 0
inputs = []
width = 200
height = 200
offset_x = 900
offset_y = 700
for x in range(offset_x, offset_x+width):
    for y in range (offset_y, offset_y+height):
        inputs.append([x, y])
mymap = [['.' for i in range(height)] for j in range(width)]

def getmap(x, y):
    return mymap[y - offset_y][x - offset_x]

def setmap(x, y, value):
    mymap[y - offset_y][x - offset_x] = value

def goodcoord(x,y):
    return x >= offset_x and x < (offset_x + width) and y >= offset_y and y < (offset_y + height)

def output(out):
    global count_points, inputs, cursor
    cur_loc = inputs[cursor]
    if out == 1:
        count_points += 1
        setmap(cur_loc[0], cur_loc[1], '#')
    cursor += 1

def test_square_corner(pos, side):
    global mymap
    for i in range(0, side):
        #print("Good Cord: " + str((pos[0], pos[1]+i)) + " " + str(goodcoord(pos[0], pos[1]+i)))
        #print("Get Map: " + str(getmap(pos[0], pos[1]+i)))
        if (not goodcoord(pos[0], pos[1]+i)) or getmap(pos[0], pos[1] + i) != "#":
            return False
        if (not goodcoord(pos[0] + i, pos[1])) or getmap(pos[0] + i, pos[1]) != "#":
            return False
        #print("Good: " + str(pos) + " " + str(i))
    return True

def run_program_part1(codes, input):
    global inputs
    
    prog = Program(codes, input, None, output)
    steps = 0
    while True:
        prog.step()
        steps += 1
        if prog.halt:
            #print("HALT")
            break
        if (steps % 1000) == 0:
            print(str(steps))

def print_map():
    global mymap
    drawmap = copy.deepcopy(mymap)

    for row in drawmap:
        print(''.join(row))
        
codes = []
with open('day19.txt') as file:
    for line in file:
        codes.extend(line.rstrip().split(","))

#print(codes)
int_codes = list(map(lambda x: int(x), codes))
#print("Program Length: " + str(len(int_codes)))
int_codes.extend([0] * 10000)
for input in inputs:
    run_program_part1(int_codes, input)
print("Num Points: " + str(count_points))
print_map()

best = [(-1, -1)] * 10
best_dist = [1000000] * 10
sizes = range(95, 105)
for i in range(0, 10):
    for x in range(offset_x, offset_x+width):
        for y in range(offset_y, offset_y+height):
            dist = x + y
            if test_square_corner((x, y), sizes[i]):
                #print("Found" + str((x, y)))
                if dist < best_dist[i]:
                    best_dist[i] = dist
                    best[i] = (x, y)
print("Closest Points: " + str(best))

# 100 -> (948, 761)
# 43 -> (405, 325)
# 40 -> (375, 301)
# 35 -> (329, 264)
# 29 -> (269, 216)
# 25 -> (233, 187)
# 20 -> (183, 147)
# 19 -> (173, 139)
# 18 -> (166, 113)
# 17 -> (156, 125)
# 16 -> (147, 118)
# 15 -> (137, 110)
# 14 -> (127, 102)
# 13 -> (117, 94)
# 12 -> (107, 86)
# 11 -> (97, 78)
# 10 -> (90, 72)
# 9 -> (80, 64)
# 8 -> (70, 56)
# 7 -> (60, 48)
# 6 -> (50, 40)
# 5 -> (40, 32)