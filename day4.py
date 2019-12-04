
start = 206938
end = 679128
count = 0
for x in range(start, end):
    sx = str(x)
    found_adjacent = False
    found_decrease = False
    prev = 0
    cur_run = 1
    for i in range(len(sx) - 1):
        if sx[i] == sx[i+1]:
            cur_run += 1
        else:
            if cur_run == 2:
                found_adjacent = True
            cur_run = 1
        if int(sx[i]) < prev:
            found_decrease = True
        prev = int(sx[i])
    if cur_run == 2:
        found_adjacent = True
    if found_adjacent and not found_decrease and int(sx[len(sx) - 1]) >= prev:
        count += 1

print(count)
    