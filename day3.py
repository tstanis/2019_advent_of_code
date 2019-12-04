rid = [[0 for i in range(0, 20000)] for j in range(0, 20000)]

def print_grid(grid):
    for row in grid[::-1]:
        print(''.join(map(lambda x: str(x), row)))

def fill(x, y, steps):
    grid[x][y] = steps

def fill_grid(wire, startx, starty):
    walk_grid(wire, startx, starty, fill)

def walk_grid(wire, startx, starty, walk_func):
    x = startx
    y = starty
    steps = 1
    for segment in wire:
        dir = segment[0:1]
        dist = int(segment[1:])
        print("Dir: " + dir + " dist: " + str(dist))
        #walk_func(x, y, steps)
        if dir == 'R':
            for i in range(x+1, x+dist+1):
                walk_func(i, y, steps)
                steps += 1
            x = x + dist
        if dir == 'L':
            for i in range(x-1, x-dist-1, -1):
                walk_func(i, y, steps)
                steps += 1
            x = x - dist
        if dir == 'U':
            for i in range(y+1, y+dist+1):
                walk_func(x, i, steps)
                steps += 1
            y = y + dist
        if dir == 'D':
            for i in range(y-1, y-dist-1, -1):
                walk_func(x, i, steps)
                steps += 1
            y = y - dist

def find_hits(wire, startx, starty):
    hits = []
    def catch_hits(x, y, steps):
        if x == startx and y == starty:
            return
        if grid[x][y] > 0:
            hits.append((x - startx, y - starty, steps, grid[x][y]))
    walk_grid(wire, startx, starty, catch_hits)
    return hits

wires = []
example1 = "R8,U5,L5,D3"
second1 = "U7,R6,D4,L4"
example2 = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
second2 = "U62,R66,U55,R34,D71,R55,D58,R83"
example3 = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
second3 = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
with open('day3.txt') as file:
    for line in file:
        wires.append(line)

#wires[0] = example3
#wires[1] = second3
fill_grid(wires[0].split(','), 1000, 1000)

hits = find_hits(wires[1].split(','), 1000, 1000)
print(hits)
best = -1
for hit in hits:
    dist = abs(hit[0]) + abs(hit[1])
    if best == -1 or dist < best:
        best = dist
print("Best: " + str(best)) 

best = -1
for hit in hits:
    total_steps = hit[2] + hit[3]
    if best == -1 or total_steps < best:
        best = total_steps
print("Best Steps: " + str(best)) 




    