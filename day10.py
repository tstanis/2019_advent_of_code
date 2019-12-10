import math
mymap = []

with open('day10.txt') as file:
    for line in file:
        mymap.append(line.rstrip())

def is_visible(x, y, to_x, to_y):
    #print("is_visible(" + str(x) + "," + str(y) + " to " + str(to_x) + "," + str(to_y))
    dx = to_x - x
    dy = to_y - y
    dirx = 1 if dx > 0 else -1
    diry = 1 if dy > 0 else -1
    absdx = abs(dx)
    absdy = abs(dy)
    factor = math.gcd(absdx, absdy)
    #print("factor=" + str(factor))
    if dx == 0:
        for i in range(y+diry, to_y, diry):
            if mymap[i][x] == '#':
                #print("FalseY")
                return False
    elif dy == 0:
        for i in range(x+dirx, to_x, dirx):
            if mymap[y][i] == '#':
                #print("FalseX " + str(i) + "," + str(y))
                return False
    # only check for diagonals if it is an equal run
    elif (factor > 1 or absdx == absdy) and factor <= min(absdx, absdy):
        if absdx < absdy:
            stepy = int(absdy / factor)
            stepx = int(absdx / factor)
            stepx = stepx if dx > 0 else -stepx
            stepy = stepy if dy > 0 else -stepy
            #print("stepx = " + str(stepx) + " stepy = " + str(stepy))
            cury = y
            for i in range(x+stepx, to_x, stepx):
                cury += stepy
                #print("Test " + str(i) + "," + str(cury))
                if mymap[cury][i] == '#':
                    #print("False Diag " + str(i) + "," + str(cury))
                    return False
        else:
            stepx = int(absdx / factor)
            stepy = int(absdy / factor)
            stepx = stepx if dx > 0 else -stepx
            stepy = stepy if dy > 0 else -stepy
            #print("stepx = " + str(stepx) + " stepy = " + str(stepy))
            cury = y
            for i in range(x+stepx, to_x, stepx):
                cury += stepy
                #print("Test " + str(i) + "," + str(cury))
                if mymap[cury][i] == '#':
                    #print("False Diag " + str(i) + "," + str(cury))
                    return False
            
    #print("True")
    return True

def calc_angle(laser_x, laser_y, asteroid_x, asteroid_y):
    return math.atan2(asteroid_x - laser_x, asteroid_y - laser_y)

def calc_dist(laser_x, laser_y, asteroid_x, asteroid_y):
    return abs(laser_x - asteroid_x) + abs(laser_y - asteroid_y)

width=len(mymap[0])
height=len(mymap)
print("Dim width=" + str(width) + " height=" + str(height))
#print(str(map))
visible = []
#print(str(visible))
total_asteroids = 0
for y in range(0, height):
    visible.append([0] * width)
    print(str(mymap[y]))
    for x in range(0, width):
        #print(str(map[y][x]))
        if mymap[y][x] == '#':
            total_asteroids += 1
            cnt = 0
            for other_y in range(0, height):
                for other_x in range(0, width):
                    if x == other_x and y == other_y:
                        continue
                    if mymap[other_y][other_x] == '#':
                        cnt += 1 if is_visible(x, y, other_x, other_y) else 0
            visible[y][x] = cnt
        else:
            visible[y][x] = 0

print("Total Asteroids: " + str(total_asteroids))
best = 0
best_x = 0
best_y = 0
best_str = ""
for y in range(0, height):
    for x in range(0, width):
        if visible[y][x] > best:
            best = visible[y][x]
            best_x = x
            best_y = y
            best_str = str(x) + "," + str(y)
print("Best Location: " + best_str)
print("Visible: " + str(best))

asteroids = {}
for y in range(0, height):
    for x in range(0, width):
        if y == best_y and x == best_x:
            continue
        else:
            if mymap[y][x] == '#':
                asteroids[(x,y)] = (calc_angle(best_x, best_y, x, y), calc_dist(best_x, best_y, x, y))

simple_list = list(asteroids.items())
simple_list = sorted(simple_list, key=lambda x: (x[1][0], -x[1][1]), reverse=True)
last_angle = 0
num = 0
skipped = []
while len(simple_list) > 0:
    while len(simple_list) > 0:
        asteroid = simple_list.pop(0)
        if asteroid[1][0] == last_angle:
            skipped.append(asteroid)
            continue
        last_angle = asteroid[1][0]
        num += 1
        print(str(num) + " -> " + str(asteroid[0]))
    simple_list.extend(skipped)
    skipped = []
    last_angle = 0