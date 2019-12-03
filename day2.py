def run_program(codes):
    pc = 0
    try:
        while True:
            opcode = codes[pc]
            if opcode == 99:
                break
            a = codes[codes[pc+1]]
            b = codes[codes[pc+2]]
            if opcode == 1:
                a = codes[codes[pc+1]]
                b = codes[codes[pc+2]]
                codes[codes[pc+3]] = a + b
            elif opcode == 2:
                codes[codes[pc+3]] = a * b
            pc += 4
    finally:
        return codes[0]

codes = []

with open('day2.txt') as file:
    for line in file:
        codes.extend(line.split(','))
original_codes = list(map(lambda x: int(x), codes))

print(original_codes)

codes = original_codes.copy()
part1 = False
if part1:
    codes[1] = 12
    codes[2] = 2


for i in range(0, 1000):
    for j in range(0, 1000):
        new_codes = original_codes.copy()
        new_codes[1] = i
        new_codes[2] = j
        result = run_program(new_codes)
        if result == 19690720:
            print("Found it " + str(i) +","+ str(j))
            print("Answer: " + str(100 * i + j))


