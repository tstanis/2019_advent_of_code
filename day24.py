import copy

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

example_part2 = """....#
#..#.
#.?##
..#..
#...."""

startstate_part2 = """###.#
..#..
#.?#.
#....
.#.#."""

def score_bugs(x):
    return 1 if x == '#' else 0

def get_num_from_side(state, dir):
    if dir[0] == -1:
        return sum(map(score_bugs, [x[4] for x in state]))
    if dir[0] == 1:
        return sum(map(score_bugs, [x[0] for x in state]))
    if dir[1] == 1:
        return sum(map(score_bugs, state[0]))
    if dir[1] == -1:
        return sum(map(score_bugs, state[4]))
    raise "Unknown dir" + str(dir)

def get_num_from_inside(state, dir):
    if dir[0] == -1:
        return score_bugs(state[2][1])
    if dir[0] == 1:
        return score_bugs(state[2][3])
    if dir[1] == -1:
        return score_bugs(state[1][2])
    if dir[1] == 1:
        return score_bugs(state[3][2])
    return "Unknown dir: " + str(dir)

def get_num_adjacent(state, x, y, parent, child):
    num = 0
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dir in dirs:
        neib = (x + dir[0], y + dir[1])
        if neib[0] >= 0 and neib[0] < len(state[0]) and neib[1] >= 0 and neib[1] < len(state):
            bugs = state[neib[1]][neib[0]]
            if bugs == '#':
                num += 1
            elif bugs == '?' and child:
                num += get_num_from_side(child, dir)
        elif parent:
            num += get_num_from_inside(parent, dir)
    return num

def print_map(mymap):
    for row in mymap:
        print(''.join(row))

def num_on_outer_edges(state):
    amount = sum(map(score_bugs, state[0])) + \
        sum(map(score_bugs, state[4])) + \
        score_bugs(state[1][0]) + \
        score_bugs(state[2][0]) + \
        score_bugs(state[3][0]) + \
        score_bugs(state[1][4]) + \
        score_bugs(state[2][4]) + \
        score_bugs(state[3][4])
    print("Num on outer: " + str(amount))
    return amount

def num_on_inner_edges(state):
    amount = score_bugs(state[1][2]) + \
        score_bugs(state[2][1]) + \
        score_bugs(state[2][3]) + \
        score_bugs(state[3][2])
    print("Num on inner: " + str(amount))
    return amount


def tick_state(state, parent, child):
    outstate = [['.' for x in range(5)] for y in range(5)]
    outstate[2][2] = '?'
    for x in range(len(state[0])):
        for y in range(len(state)):
            b = get_num_adjacent(state, x, y, parent, child)
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

blank_state_txt = """.....
.....
..?..
.....
....."""

blank_state = [list(x) for x in blank_state_txt.split("\n")]
class Stack:
    def __init__(self, state, layer_id):
        self.state = state
        self.parent = None
        self.child = None
        self.next_state = None
        self.layer_id = layer_id

    def get_parent(self):
        return self.parent

    def get_child(self):
        return self.child

    def create_parent(self):
        self.parent = copy.deepcopy(blank_state)

    def create_child(self):
        self.child = copy.deepcopy(blank_state)

    def print_stack(self, prev=None):
        if self.parent and self.parent != prev:
            self.parent.print_stack(self)
        print("Depth " + str(self.layer_id) + ":")
        print_map(self.state)
        if self.child and self.child != prev:
            self.child.print_stack(self)
        

    def commit_tick(self, prev):
        if self.next_state:
            self.state = self.next_state
            self.next_state = None
        else:
            print("Nothing to commit layer " + str(self.layer_id))
        if self.parent and self.parent != prev:
            self.parent.commit_tick(self)
        if self.child and self.child != prev:
            self.child.commit_tick(self)

    def tick(self, prev):
        self.next_state = tick_state(self.state, self.parent.state if self.parent else None, \
            self.child.state if self.child else None)
        if self.parent and self.parent != prev:
            self.parent.tick(self)
        elif not self.parent and num_on_outer_edges(self.state) > 0:
            self.parent = Stack(copy.deepcopy(blank_state), self.layer_id - 1)
            self.parent.child = self
            self.parent.tick(self)

        if self.child and self.child != prev:
            self.child.tick(self)
        elif not self.child and num_on_inner_edges(self.state) > 0:
            self.child = Stack(copy.deepcopy(blank_state), self.layer_id + 1)
            self.child.parent = self
            self.child.tick(self)
        if prev == None:
            self.commit_tick(None)
    
    def num_bugs(self, prev=None):
        num = 0
        for y in range(len(self.state)):
            for x in range(len(self.state[y])):
                num += score_bugs(self.state[y][x])
        if self.parent and self.parent != prev:
            num += self.parent.num_bugs(self)
        if self.child and self.child != prev:
            num += self.child.num_bugs(self)
        return num



previous = set()


state = [list(x) for x in startstate_part2.split("\n")]
print_map(state)
stack = Stack(state, 0)
for i in range(200):
    print("Minute " + str(i))
    stack.tick(None)
    stack.print_stack()
    #tupled = tuple([j for sub in state for j in sub])
    #if tupled in previous:
    #    print("DUPLICATE: " + str(''.join(tupled)))
    #    print("BIODIVERSITY: " + str(calc_biodiversity(tupled)))
    #    exit()
    #else:
    #    previous.add(tupled)

print("TOTAL BUGS: " + str(stack.num_bugs()))