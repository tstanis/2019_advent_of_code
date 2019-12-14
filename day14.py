import math
from collections import defaultdict
from functools import reduce

example = """9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL"""

example2 = """157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""

example3 = """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF"""

example4 = """171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX"""

realinput = """1 BNZK => 2 NMDF
3 KPQPD => 4 GSRWZ
2 ZRSFC => 7 SRGL
5 XNPDM, 1 FGCV => 7 HMTC
18 LHTNC, 1 WGXGV => 9 CDKF
24 BMQM => 5 FKHRJ
2 LFPNB => 6 XNSVC
9 ZKFRH, 4 XGPLN, 17 SPQP, 2 GVNTZ, 1 JMSCN, 9 SHQN, 1 DZLWC, 18 MSKQ => 7 TXDQK
2 QFTW => 9 JPZT
1 KJCK, 1 TFKZ, 2 XNSVC => 7 GQRB
16 JPZT, 3 DCPW => 7 KJCK
24 LGKPJ, 11 CDKF, 2 HVZQM => 7 RNXJ
1 NMDF, 16 DBLGK, 1 HVZQM => 7 ZKFRH
4 TXDQK, 55 TNZT, 39 KDTG, 6 NVBH, 15 SDVMB, 53 XVKHV, 28 FKHRJ => 1 FUEL
3 CDKV, 11 FGCV => 1 NVBH
3 SPNRW, 7 JMSCN => 9 XMCNV
14 FGCV, 3 CQLRM, 1 TFKZ => 6 PQVBV
5 KJCK, 10 DCPW => 7 DSKH
5 NMDF, 1 TFKZ => 5 DZLWC
1 TNZT => 6 RTSBT
178 ORE => 6 XVLBX
1 SPNRW => 5 CWKH
15 ZRSFC, 2 PQVBV, 2 SRGL => 3 SPNRW
1 SHQN, 7 XNSVC => 4 QWMZQ
5 NVBH, 41 SHQN => 4 BNZK
1 CDKV, 6 KJCK => 4 TNZT
5 ZTBG, 1 HVZQM, 27 CDKV, 1 LHTNC, 2 RTSBT, 2 SHQN, 26 DZLWC => 9 KDTG
11 CDKV => 7 SHQN
13 QWMZQ, 19 FCFG => 7 GVNTZ
1 SHQN, 4 XNSVC => 9 ZRSFC
2 ZKFRH, 9 HVZQM, 1 KJCK, 3 GQRB, 11 DBLGK, 8 DZLWC, 2 SPQP, 5 RNXJ => 8 SDVMB
5 SPNRW => 7 JMSCN
2 XVLBX, 19 KPQPD => 7 XNPDM
2 JPZT => 8 CDKV
1 GQRB => 7 MSKQ
1 SHQN, 13 DSKH => 3 MHQVS
9 JPZT => 8 LFPNB
15 SPNRW, 4 GQRB => 9 SPQP
1 JPZT => 3 TFKZ
1 BMQM => 6 FGCV
24 FKHRJ => 9 DCPW
2 GSRWZ => 8 XGPLN
5 QPSDR, 1 XVLBX => 6 BMQM
128 ORE => 7 QPSDR
2 LHTNC, 6 FCFG, 5 GVNTZ => 7 ZTBG
9 KJCK, 6 MHQVS, 5 NVBH => 6 KRDGK
3 HMTC, 4 QWMZQ => 2 FCFG
4 WGXGV, 5 PQVBV => 1 LGKPJ
42 XVLBX => 5 CQLRM
1 CWKH => 9 DBLGK
1 KRDGK, 2 GQRB, 12 TFKZ => 5 LHTNC
1 CQLRM, 1 HMTC => 8 WGXGV
116 ORE => 1 QFTW
13 XMCNV => 5 XVKHV
12 LGKPJ, 8 FKHRJ => 9 HVZQM
5 QPSDR => 6 KPQPD"""

def parse_bit(bit):
    parts = bit.split(" ")
    return (int(parts[0]), parts[1])

class Rule:
    
    def __init__(self, output, inputs):
        self.output = output
        self.inputs = inputs
        self.input_rules = []

    def __init__(self, str_rule):
        self.inputs = []
        parts = str_rule.split(" => ")
        ingredients = parts[0].split(", ")
        self.output = parse_bit(parts[1])
        for i in ingredients:
            self.inputs.append(parse_bit(i))
        self.input_rules = []

    def get_ore_cost(self, count, leftovers):
        #print("Need %d %s" % (count, self.output[1]))
        batches = math.ceil(count / self.output[0])
        remain = (batches * self.output[0]) - count
        ore_cost = 0
        for i in range(0, len(self.inputs)):
            input = self.inputs[i]
            if input[1] == 'ORE':
                ore_cost += input[0] * batches
            else:
                needed = input[0] * batches
                #print("Gen %d %s" % (needed, input[1]))
                if input[1] in leftovers:
                    leftover_available = leftovers[input[1]]
                    needed = needed - leftover_available
                    leftovers[input[1]] = -needed if needed < 0 else 0
                    #print("Using %d leftovers of %s" % ((input[0] * batches) - needed, input[1]))
                    #print(str(leftovers))
                    if needed <= 0:
                        continue
                input_rule = self.input_rules[i]
                ore_cost += input_rule.get_ore_cost(needed, leftovers)
        #print("Cost %d ORE for %d %s." % (ore_cost, batches * self.output[0], self.output[1]))
        if remain: 
            leftovers[self.output[1]] += remain
            #print("Adding %d leftovers of %s" % (remain, self.output[1]))
            #print(str(leftovers))
        return ore_cost

    def get_ingredient_needs(self, count):
        print("Need %d %s" % (count, self.output[1]))
        needs = {}
        ore_needs = 0
        for input in self.inputs:
            if input[1] == 'ORE':
                ore_needs += math.ceil(input[0] / self.output[0]) * count
            else:
                needs[input[1]] = input[0] * count
        return needs, ore_needs

    def __str__(self):
        out = "Rule %d %s: " % self.output
        for i in range(0, len(self.inputs)):
            input = self.inputs[i]
            out += "["
            if input[1] != 'ORE':
                out += "(%d %s) -> %s" % (input[0], input[1], str(self.input_rules[i]))
            else:
                out += "(%d ORE)" % (input[0])
            out += "]"
        return out

    def __repr__(self):
        return self.__str__()
    
rules = []
for line in realinput.split("\n"):
    rules.append(Rule(line))

output_map = {}
for rule in rules:
    output_map[rule.output[1]] = rule

for rule in rules:
    for input in rule.inputs:
        if input[1] != 'ORE':
            src = output_map[input[1]]
            rule.input_rules.append(src)


print(str(output_map['FUEL']))

cost_for_one = output_map['FUEL'].get_ore_cost(1, defaultdict(int))
print(str(cost_for_one))

ore = 1000000000000
total_ore_cost = 0
fuel = 0
leftovers = defaultdict(int)
i = 0
pre_run = 0
while ore > 0:
    i += 1
    if i % 10000 == 0:
        print(str(ore))
    ore_cost = output_map['FUEL'].get_ore_cost(1, leftovers)
    total_ore_cost += ore_cost
    #print(str(leftovers))
    num_leftovers = sum(leftovers.values())
    #print("Num Leftovers: " + str(num_leftovers))
    ore -= ore_cost
    if ore > 0:
        fuel += 1
    if num_leftovers == 0 and pre_run == 0:
        used_ore = total_ore_cost
        print("Clean Burn: %d for %d" % (used_ore, fuel))
        batches = 1000000000000 / used_ore
        ore = 1000000000000 - (batches * used_ore)
        fuel = batches * fuel
        pre_run = 1
        continue
    #print("Ore Cost " + str(ore_cost))
    #print(str(leftovers))
print("Amount of Fuel : %d" % (fuel))
    


