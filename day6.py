from collections import defaultdict

example = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""

edges = []
with open('day6.txt') as file:
    for line in file:
        parts = line.split(")")
        edges.append((parts[0], parts[1].rstrip()))

graph = defaultdict(list)
reverse_graph = defaultdict(list)
for edge in edges:
    graph[edge[1]].append(edge[0])
    reverse_graph[edge[0]].append(edge[1])

visited = defaultdict(int)

def count_orbits(node):
    count = 1
    for link in graph[node]:
        count += count_orbits(link)
    return count

total_orbits = 0
for node in list(graph.keys()):
    orbits = count_orbits(node) - 1
    total_orbits += orbits

print("Num Nodes: " + str(len(graph.keys())))
print("Total: " + str(total_orbits))

open_set = []
results = []
visited = defaultdict(int)
open_set.append(['YOU'])
while len(open_set) > 0:
    cur_path = open_set.pop()
    strpath = ''.join(cur_path)
    visited[strpath] = 1
    for link in graph[cur_path[-1]]:
        if link in cur_path:
            continue
        next_path = cur_path.copy()
        next_path.append(link)
        if link == 'SAN':
            results.append(next_path)
        elif visited[''.join(next_path)] != 1:
            open_set.append(next_path)

    for link in reverse_graph[cur_path[-1]]:
        if link in cur_path:
            continue
        next_path = cur_path.copy()
        next_path.append(link)
        if link == 'SAN':
            results.append(next_path)
        elif visited[''.join(next_path)] != 1:
            open_set.append(next_path)

print(str(results))
print('Paths Visited = ' + str(len(visited.keys())))
for result in results:
    print(len(result) - 3)