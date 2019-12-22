import copy

def find_portals(themap):
    inportals = {}
    outportals = {}
    print("width = " + str(len(themap[0])))
    for y in range(0, len(themap)):
        for x in range(0, len(themap[y])):
            if themap[y][x] == ".":
                portal_dest = outportals if (x == 2 or y == 2 or y == len(themap) - 3 or x == len(themap[0]) - 3) else inportals
                name = None
                if themap[y-1][x].isupper():
                    name = themap[y-2][x] + themap[y-1][x]
                elif themap[y+1][x].isupper():
                    name = themap[y+1][x] + themap[y+2][x]
                elif themap[y][x-1].isupper():
                    name = themap[y][x-2] + themap[y][x-1]
                elif themap[y][x+1].isupper():
                    name = themap[y][x+1] + themap[y][x+2]
                if name:
                    portal_dest[name] = (x, y)
    return inportals, outportals

def find_path_lengths_from(themap, position_to_portal, name_to_portals):
    paths = {}
    for portal, ends in name_to_portals.items():
        portal_sides = {ends[0] : explore(ends[0], 0, themap, {}, position_to_portal), \
            ends[1] : explore(ends[1], 0, themap, {}, position_to_portal)}
        paths[portal] = portal_sides
    return paths

def explore(pos, distance, themap, visited, portals):
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]
    found = []
    next_distance = distance + 1
    visited[pos] = 1
    for dir in dirs:
        dest = tuple(map(sum,zip(dir,pos)))
        if dest not in visited and themap[dest[1]][dest[0]] == ".":
            if dest in portals:
                found.append((next_distance, portals[dest], dest))
            else:
                found.extend(explore(dest, next_distance, themap, visited, portals))
    return found

def print_map():
    global mymap
    drawmap = copy.deepcopy(mymap)

    for row in drawmap:
        print(''.join(row))

def find_shortest_path(depth, cur_name, cur_loc, end_portal_name, themap, name_to_portals, position_to_portal, paths, length, visited):
    indent = " " * depth
    print(indent + "Find Shortest " + cur_name)
    visited[cur_name] = 1
    results = []
    for dist, choice, pos in paths[cur_name][cur_loc]:
        print(indent + choice)
        if choice == end_portal_name:
            results.append(length + dist)
        elif not choice in visited:
            p = name_to_portals[choice]
            otherside = p[0] if p[0] != pos else p[1]
            subresult = find_shortest_path(depth+1, choice, otherside, end_portal_name, themap, name_to_portals, \
                position_to_portal, paths, length + dist + 1, visited.copy())
            if subresult:
                results.append(subresult)
    if len(results) > 0:
        return min(results)
    else:
        return None




mymap = []
with open('day20.txt') as file:
    for line in file:
        mymap.append(list(line.rstrip('\n')))

inportals, outportals = find_portals(mymap)
position_to_portal = {value: key for key, value in inportals.items()}
position_to_portal.update({value: key for key, value in outportals.items()})
name_to_portals = {}
for portal_name, pos in inportals.items():
    if portal_name in outportals:
        name_to_portals[portal_name] = (pos, outportals[portal_name])
name_to_portals['AA'] = (outportals['AA'], (0,0))

print_map()

print("IN " + str(inportals))
print("OUT " + str(outportals))

print("NAME TO PORTAL: " + str(name_to_portals))
paths = find_path_lengths_from(mymap, position_to_portal, name_to_portals)
print("PATHS: " + str(paths))

shortest = find_shortest_path(0, "AA", name_to_portals['AA'][0], "ZZ", mymap, name_to_portals, position_to_portal, paths, 0, {})
print("SHORTEST: "+ str(shortest))