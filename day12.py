import copy
import math
moons = []

class Moon:
    def __init__(self, start_pos):
        self.pos = start_pos
        self.velocity = [0,0,0]
    
    def apply_gravity(self, other_moons):
        for moon in other_moons:
            for i in [0,1,2]:
                self.velocity[i] += 1 if self.pos[i] < moon.pos[i] else (-1 if self.pos[i] > moon.pos[i] else 0)

    def apply_velocity(self):
        for i in [0,1,2]:
            self.pos[i] += self.velocity[i]

    def energy(self):
        potential = sum(map(abs, self.pos))
        kinetic = sum(map(abs, self.velocity))
        return potential * kinetic 

    def print(self):
        print("pos=<x=%02d, y=%02d, z=%02d>, velocity=<x=%02d, y=%02d, z=%02d> energy = %d %d" % (tuple(self.pos) + tuple(self.velocity) + (self.energy(), 0)))


def time_step():
    for moon in moons:
        other_moons = moons.copy()
        other_moons.remove(moon)
        moon.apply_gravity(other_moons)
    for moon in moons:
        moon.apply_velocity()
    total_energy = 0
    for moon in moons:
        total_energy += moon.energy()
    return total_energy

def state_matches(state1, state2, dims):
    for i in range(0, len(state1)):
        for d in dims:
            if state1[i].pos[d] != state2[i].pos[d] or state1[i].velocity[d] != state2[i].velocity[d]:
                return False
    return True

#moons.append(Moon([-1,0, 2]))
#moons.append(Moon([2,-10,-7]))
#moons.append(Moon([4,-8, 8]))
#moons.append(Moon([3,5, -1]))

#moons.append(Moon([-8,-10, 0]))
#moons.append(Moon([5,5,10]))
#moons.append(Moon([2,-7, 3]))
#moons.append(Moon([9,-8, -3]))

moons.append(Moon([1,4, 4]))
moons.append(Moon([-4,-1,19]))
moons.append(Moon([-15,-14, 12]))
moons.append(Moon([-17,1, 10]))

initial_state = copy.deepcopy(moons)

for moon in moons:
    moon.print()
i = 0
found = [0, 0, 0]
delta = [0, 0, 0]
while found[0]<2 or found[1]<2 or found[2]<2:
    if i % 100000 == 0:
        print(str(i))
        print("x=[" + str([moons[0].pos[0], moons[1].pos[0], moons[2].pos[0], moons[3].pos[0]]))
    energy = time_step()
    for dim in range(0, 3):
        if state_matches(initial_state, moons, [dim]):
            print("Initial State Reached for dim %d!  %d" % (dim, i))
            for moon in moons:
                moon.print()
            found[dim] += 1
            if found[dim] == 1:
                delta[dim] = i + 1
    i += 1
print(str(delta))

def lcm(a):
    lcm = a[0]
    for i in a[1:]:
        lcm = int(lcm*i/math.gcd(lcm, i))
    return lcm

print(str(lcm(delta)))