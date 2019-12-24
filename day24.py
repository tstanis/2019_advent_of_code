example = """....#
#..#.
#..##
..#..
#...."""

startstate = """###.#
..#..
#..#.
#....
.#.#."""

def get_num_adjacent(state, x, y):
    num = 0
    if x > 0 and state[y][x-1] == '#':
        num += 1
    if y > 0 and state[y-1][x] == '#':
        num += 1
    if x < len(state[0]) - 1 and state[y][x+1] == '#':
        num += 1
    if y < len(state) - 1 and state[y+1][x] == '#':
        num += 1
    return num

def print_map(mymap):
    for row in mymap:
        print(''.join(row))     

def tick(state):
    outstate = [['.' for x in range(5)] for y in range(5)]
    for x in range(len(state[0])):
        for y in range(len(state)):
            b = get_num_adjacent(state, x, y)
            if state[y][x] == '#':
                outstate[y][x] = '#' if b == 1 else '.'
            elif state[y][x] == '.':
                outstate[y][x] = '#' if b == 1 or b == 2 else '.'
    return outstate

def calc_biodiversity(tupled_state):
    b = 0
    for i in range(len(tupled_state)):
        if tupled_state[i] == '#':
            b += pow(2, i)
    return b

previous = set()

state = [list(x) for x in startstate.split("\n")]
print_map(state)
for i in range(100):
    print("")
    state = tick(state)
    print_map(state)
    tupled = tuple([j for sub in state for j in sub])
    if tupled in previous:
        print("DUPLICATE: " + str(''.join(tupled)))
        print("BIODIVERSITY: " + str(calc_biodiversity(tupled)))
        exit()
    else:
        previous.add(tupled)