
def run_program(codes, input):
    pc = 0
    output = []

    while True:
        instruction = str(codes[pc])
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
            print("BREAK")
            break
        #print("MODES = " + str(modes))
        if opcode == 1 or opcode == 2 or opcode == 4 or opcode == 5 or opcode == 6 or opcode == 7 or opcode == 8:
            if modes[0] == 0:
                a = codes[codes[pc+1]]
            else:
                a = codes[pc+1]
        if opcode == 1 or opcode == 2 or opcode == 5 or opcode == 6 or opcode == 7 or opcode == 8:
            if modes[1] == 0:
                b = codes[codes[pc+2]]
            else:
                b = codes[pc+2]
        if opcode == 1:
            #print(str(pc) + " " + instruction + " ADD " + str(a) + " " + str(b) + "->" + str(codes[pc+3]))
            codes[codes[pc+3]] = a + b
            pc += 4
        elif opcode == 2:
            #print(str(pc) + " " + instruction + " MULTIPLY")
            codes[codes[pc+3]] = a * b
            pc += 4
        elif opcode == 3:
            value = input.pop()
            #print(str(pc) + " " + instruction + " STORE " + str(value) + " @ " + str(codes[pc+1]))
            codes[codes[pc+1]] = value
            pc += 2
        elif opcode == 4:
            print(str(pc) + " " + instruction + " OUTPUT " + str(a))
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
            codes[codes[pc+3]] = 1 if a < b else 0
            pc += 4
        elif opcode == 8: # equals
            codes[codes[pc+3]] = 1 if a == b else 0
            pc += 4
                
codes = []
with open('day5.txt') as file:
    for line in file:
        codes.extend(line.split(','))

int_codes = list(map(lambda x: int(x), codes))
for i in range(0, len(codes)):
    print(str(i) + " " + str(codes[i]))

run_program(int_codes, [5])