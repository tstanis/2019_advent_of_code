import copy
import heapq
from timeit import default_timer as timer
from collections import defaultdict

# Found Answer: 4258 127.77571289800001
# Found Answer: 4256 734.3117911439999
# Found Answer: 4252 1032.649414664
mymap = []
with open('day18.txt') as file:
    for line in file:
        mymap.append(list(line.rstrip()))

mymap[40][40] = '#'
mymap[41][40] = '#'
mymap[39][40] = '#'
mymap[40][39] = '#'
mymap[40][41] = '#'

keys = {}
doors = {}
starts = []
for cell in [(39, 39), (41, 39), (41, 41), (39, 41)]:
    mymap[cell[1]][cell[0]] = '@'

def find_map_bits():
    global mymap, keys, doors, starts
    for y in range(0, len(mymap)):
        for x in range(0, len(mymap[0])):
            element = mymap[y][x]
            if element != "." and element != "#":
                if element == '@':
                    starts.append((x, y))
                elif element.islower():
                    keys[element] = (x, y)
                else:
                    doors[element] = (x, y)

def find_path(begin, end, curmap):
    open = [(begin, [])]
    visited = {}
    while len(open) > 0:
        #print(str(open))
        spot, path = open.pop(0)
        choices = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for choice in choices:
            dest = tuple(map(lambda i, j: i + j, spot, choice))
            result = curmap[dest[1]][dest[0]]
            #print(str(result) + " -> " + str(dest))
            if dest == end:
                path.append(dest)
                return path
            elif result == '.' or result == '@':
                if not dest in visited:
                    newpath = copy.copy(path)
                    newpath.append(dest)
                    open.append((dest, newpath))
        visited[spot] = 1
    return None

def find_path_length(begin, end, curmap, opened_doors, maxlen):
    opennodes = [(begin, 0)]
    visited = {' '}
    best_len = None
    while len(opennodes) > 0:
        #opennodes.sort(key= lambda x: abs(end[0] - x[0][0]) + abs(end[1] - x[0][1]))
        #print(str(opennodes))
        spot, path_len = opennodes.pop(0)
        if maxlen and path_len > maxlen:
            continue
        if best_len and path_len >= best_len:
            continue
        choices = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for choice in choices:
            dest = (choice[0] + spot[0], choice[1] + spot[1])
            #print(str(spot) + " -> " + str(dest))
            if dest == end:
                #print("Found End: " + str(path_len))
                if not best_len or path_len < best_len:
                    best_len = path_len + 1
            else:
                result = curmap[dest[1]][dest[0]]
                if result == '#':
                    continue
                elif result == '.' or result == '@' or result.islower() or result.upper() in opened_doors:
                    if not dest in visited:
                        next = (dest, path_len + 1)
                        opennodes.append(next)
        visited.add(spot)
    return best_len

def print_map(curmap, inters):
    global mymap
    drawmap = copy.deepcopy(curmap)
    if inters:
        for inter in inters:
            drawmap[inter[1]][inter[0]] = "O"
    for row in drawmap:
        print(''.join(row))

def move(oldpos, newpos, curmap):
    curmap[oldpos[1]][oldpos[0]] = "."
    curmap[newpos[1]][newpos[1]] = '@'

# best_path_cache[(loc, remain_keys)] = best_length
best_path_cache = {}
best_path_cache_hit = 0
best_path_cache_miss = 0
def find_best_path(locs, curkeys, curmap, inter_map, opendoors, depth):
    global best_path_cache_hit, best_path_cache_miss
    cache_key = (tuple(locs), tuple(curkeys))
    if cache_key in best_path_cache:
        #print("Cache Hit!")
        best_path_cache_hit += 1
        return best_path_cache[cache_key]
    else:
        best_path_cache_miss += 1

    start = timer()
    open_nodes = [(0, None, locs, 0, curkeys, opendoors)]
    heapq.heapify(open_nodes)
    best_len = 10000 #4252
    i = 0
    while len(open_nodes) > 0:
        #print(str(open_nodes))
        i += 1
        if i % 10000 == 0:
            #max_distance = max(open_nodes, key=lambda x: x[3])[3]
            print(str(i) + " best dist = " + str(best_len) + " cache hit/miss" + str(best_path_cache_hit) + "/" + str(best_path_cache_miss) + " " + str(timer() - start))
            #open_nodes.append(open_nodes.pop(0))
        priority, key, locs, path_len, curkeys, opendoors = heapq.heappop(open_nodes)
        if best_len != None and path_len > best_len:
            continue
        nextkeys = curkeys.copy()
        nextopendoors = opendoors.copy()
        if key:
            del nextkeys[key]
            nextopendoors.add(key.upper())
        if key and len(nextkeys.keys()) > 3:
            #print(''.join([" "] * depth) + "Find Best Path " + str(loc) + " " + str(len(nextkeys.keys())))
            subcall_result = find_best_path(locs.copy(), nextkeys, curmap, inter_map, nextopendoors, depth + 1)
            #print(''.join([" "] * depth) + "Result " + str(subcall_result))
            path_len += subcall_result
            nextkeys = {}

        if len(nextkeys.keys()) == 0:
            if not best_len or path_len < best_len:
                if depth < 5:
                    print("Found Answer(" + str(depth) + "): " + str(path_len) + " " + str(timer() - start))
                best_len = path_len 
            else:   
                continue
        choices_by_loc = {}
        for loc in locs:
            choices_by_loc[loc] = find_key_choices(nextkeys.copy(), curmap, loc, nextopendoors, inter_map, 0 if not best_len else best_len - path_len)
        #print ("Choices: " + str(choices))
        #print("Keys: " + str(nextkeys))
        for loc, choices in choices_by_loc.items():
            if len(choices) > 0:
                for key, dist, thestart in choices:
                    #print("Choice %s dist %d" % (key, dist))
                    priority = (best_len - (path_len+dist), len(nextkeys))
                    heapq.heappush(open_nodes, (priority, key, [nextkeys[key] if oldloc==loc else oldloc for oldloc in locs], path_len+dist, nextkeys, nextopendoors))
    best_path_cache[cache_key] = best_len
    return best_len

cache = {}
def find_key_choices(curkeys, curmap, curstart, opened_doors, inter_map, max_len):
    cache_key = (curstart, tuple(curkeys))
    if cache_key in cache:
        return list(filter(lambda x: not max_len or x[1] <= max_len, cache[cache_key]))
    options = []
    for key, loc in curkeys.items():
        #path_len_old = find_path_length(curstart, loc, curmap, opened_doors, max_len)
        path_len = find_path_length_using_inters(curstart, loc, curmap, opened_doors, inter_map, None)
        #if path_len != path_len_old:
        #    print("MISMATCH: old=" + str(path_len_old) + " new= " + str(path_len) + " " + str(curstart) + " " + str(loc) + " " + str(opened_doors) + " " + str(max_len))
        if path_len:
            options.append((key, path_len, curstart))
    cache[cache_key] = options.copy()
    return list(filter(lambda x: not max_len or x[1] <= max_len, options))

def find_intersections(themap):
    print("Dim %d, %d" % (len(mymap[0]), len(mymap)))
    results = set()
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for y in range(1, len(mymap)-1):
        for x in range(1, len(mymap[0])-1):
            if themap[y][x].islower():
                results.add((x,y))
                continue
            if themap[y][x] != '.' and themap[y][x] != '@':
                continue
            #print("%d, %d" % (x, y))
            count_dots = 0
            for dir in dirs:
                dirx = x + dir[0]
                diry = y + dir[1]
                if themap[diry][dirx] == "." or themap[diry][dirx] == "@":
                    count_dots += 1
            if count_dots >= 3:
                results.add((x,y))
    return results

def build_intersection_map(themap, inters):
    # graph with entry points based on location...
    # { intersection: [(connection1_pos, distance, [door1, ...]), ...] }
    intersection_map = defaultdict(list)
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for inter in inters:
        open_nodes = [(inter, [], 0, set())]
        while len(open_nodes) > 0:
            cur_loc, doors, distance, visited = open_nodes.pop(0)
            visited.add(cur_loc)
            for dir in dirs:
                next_loc = (cur_loc[0] + dir[0], cur_loc[1] + dir[1])
                if next_loc in visited:
                    continue
                elif next_loc in inters:
                    intersection_map[inter].append((next_loc, distance+1, doors.copy()))
                elif themap[next_loc[1]][next_loc[0]] == "." or \
                    themap[next_loc[1]][next_loc[0]] == "@" or \
                    themap[next_loc[1]][next_loc[0]].islower() or \
                    themap[next_loc[1]][next_loc[0]].isupper():
                    nextdoors = doors.copy()
                    if themap[next_loc[1]][next_loc[0]].isupper():
                        nextdoors.append(themap[next_loc[1]][next_loc[0]])
                    open_nodes.append((next_loc, nextdoors, distance + 1, visited.copy()))
    return intersection_map
                
def get_reachable_inters(themap, inters, loc, end):
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    reachable = {}
    open_nodes = [(loc, 0, [])]
    visited = set()
    while len(open_nodes) > 0:
        loc, distance, doors = open_nodes.pop(0)
        visited.add(loc)
        for dir in dirs:
            next_loc = (loc[0] + dir[0], loc[1] + dir[1])
            map_value = themap[next_loc[1]][next_loc[0]]
            if next_loc in visited:
                continue
            elif next_loc == end:
                reachable[end] = (distance+1, doors)
            elif next_loc in inters:
                reachable[next_loc] = (distance+1, doors)
            elif map_value == "." or map_value.islower() or map_value.isupper():
                nextdoors = doors.copy()
                if map_value.isupper():
                    nextdoors.append(map_value)
                open_nodes.append((next_loc, distance+1, nextdoors))
    return reachable

def cull_reachable_by_open_doors(reachable, opened_doors):
    result = reachable.copy()
    for inter, path_meta in reachable.items():
        for door in path_meta[1]:
            if not door in opened_doors:
                del result[inter]
                break
    return result

def fill_deadends(themap):
    #print("Dim %d, %d" % (len(mymap[0]), len(mymap)))
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    anyfilled = -1
    while anyfilled != 0:
        anyfilled = 0
        for y in range(1, len(mymap)-1):
            for x in range(1, len(mymap[0])-1):
                if themap[y][x] != '.':
                    continue
                #print("%d, %d" % (x, y))
                count_walls = 0
                for dir in dirs:
                    dirx = x + dir[0]
                    diry = y + dir[1]
                    if themap[diry][dirx] == "#":
                        count_walls += 1
                if count_walls >= 3:
                    anyfilled += 1
                    themap[y][x] = '#'


def find_path_length_using_inters(begin, end, curmap, opened_doors, inters, maxlen):
    starts = get_reachable_inters(curmap, inters, begin, end)
    #print("STARTS: " + str(starts))
    starts = cull_reachable_by_open_doors(starts, opened_doors)
    if end in starts:
        #print("SHORTCIRCUIT: " + str(starts[end][0]))
        return starts[end][0]
    ends = get_reachable_inters(curmap, inters, end, None)
    ends = cull_reachable_by_open_doors(ends, opened_doors)
    ends[end] = (0, [])
    #print("ENDS: " + str(ends))
    opennodes = []
    for inter, path_meta in starts.items():
        opennodes.append((inter, path_meta[0], set()))
    best_len = None
    while len(opennodes) > 0:
        spot, path_len, visited = opennodes.pop(0)
        #print("Cur " + str(spot) + " " + str(path_len) + " " + str(visited))
        visited.add(spot)
        if maxlen and path_len > maxlen:
            continue
        if best_len and path_len >= best_len:
            continue
        if spot in ends:
            #print("DISTANCE: " + str(path_len))
            #print("ENDS: " + str(ends[spot]))
            path_len += ends[spot][0]
            if (not best_len or path_len < best_len) and (not maxlen or path_len < maxlen):
                best_len = path_len
            continue
            
        choices = inters[spot]
        #print("Choices: " + str(choices))
        for choice in choices:
            dest, distance, doors = choice
            #print("CHOICE " + str(dest) + " " + str(distance))
            if not all(door in opened_doors for door in doors):
                continue
            if dest in visited:
                continue
            opennodes.append((dest, path_len+distance, visited.copy()))
    return best_len

fill_deadends(mymap)
inters = find_intersections(mymap)
print_map(mymap, {})
find_map_bits()
inter_map = build_intersection_map(mymap, inters)
print("INTERSECTION_MAP ")
for inter, info in inter_map.items():
    print(str(inter) + " -> " + str(info))
print("NUM INTERSECTIONS: " + str(len(inter_map.keys())))
print("STARTS: " + str(starts))
print("FIRST INTERSECTION[0]: " + str(get_reachable_inters(mymap, inter_map.keys(), starts[0], None)))
print("Doors: " + str(doors))
print("Keys: " + str(keys))
from_test = (40, 40)
#for key, inter in keys.items(): #[('o', (31, 39))]:
#    open_doors = {'A', 'B', 'C', 'D', 'E', 'F', 'G'}
#    path_old = find_path_length(from_test, inter, mymap, open_doors, None)
#    path_new = find_path_length_using_inters(from_test, inter, mymap, open_doors, inter_map, None)
#    print("Path Distance " + str(key) + " " + str(inter) + ": " + str(path_old) + " " + str(path_new) )

visited = {}
#choices = find_key_choices(keys, mymap, start, {}, inter_map, None)
#print(str(choices))
results = find_best_path(starts, keys, mymap, inter_map, set(), 0)
print("RESULTS: " + str(results))