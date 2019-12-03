total_mass = 0

with open('2019_day1.txt') as file:
    for line in file:
        mass = int(int(line) / 3) - 2
        total_mass += mass
print("Part 1: " + str(total_mass))

total_mass = 0
with open('2019_day1.txt') as file:
    for line in file:
        mass = int(int(line) / 3) - 2
        total_mass += mass
        residual_mass = mass
        while residual_mass > 0:
            residual_mass = int(residual_mass / 3) - 2
            if residual_mass > 0:
                total_mass += residual_mass

print("Part 2: " + str(total_mass))
