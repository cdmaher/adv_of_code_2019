import sys
import copy
import math
from sets import Set


class Reaction:
    def __init__(self, inputs, output):
        self.inputs = inputs
        self.outputs = output

    def __str__(self):
        strInputs = ''
        for inp in self.inputs:
            strInputs += str(self.inputs[inp]) + ' ' + inp + ', '
        return strInputs + '=> ' + str(
            self.outputs[1]) + ' ' + self.outputs[0] + '\n'

    __repr__ = __str__


file = open(sys.argv[1], 'r')
lines = file.readlines()

reactions = []
for line in lines:
    splitLine = line.strip("\r\n").replace('>', '').split('=')
    inputs = splitLine[0].split(',')
    output = splitLine[1].lstrip(' ').split(' ')
    inputComps = {}
    for inp in inputs:
        components = inp.lstrip(' ').rstrip(' ').split(' ')
        inputComps[components[1]] = int(components[0])
    reactions.append(Reaction(inputComps, (output[1], int(output[0]))))

print 'Reactions: \n' + str(reactions)

elementStore = {}
elementStore['ORE'] = 1000000000000

oreForX = {}


def getOreRequirements(element, amount):
    amountOre = 0
    for reaction in reactions:
        if (reaction.outputs[0] == element):
            reactionsNeeded = int(
                math.ceil((amount * 1.0) / reaction.outputs[1]))
            leftover = amount % reaction.outputs[1]
            extraProduce = 0 if leftover == 0 else reaction.outputs[1] - leftover
            if element not in elementStore:
                elementStore[element] = 0
            for input in reaction.inputs:
                inputNeeded = reaction.inputs[input] * reactionsNeeded
                if input in elementStore:
                    takeFromStore = max(0, inputNeeded - elementStore[input])
                    elementStore[input] = max(
                        0, elementStore[input] - inputNeeded)
                    inputNeeded = takeFromStore
                if input == 'ORE':
                    amountOre += inputNeeded
                    elementStore['ORE'] -= amountOre
                    if element not in oreForX:
                        oreForX[element] = amountOre
                    else:
                        oreForX[element] = oreForX[element] + amountOre
                else:
                    amountOre += getOreRequirements(
                        input,
                        inputNeeded,
                    )
            elementStore[element] = elementStore[element] + extraProduce
    # print 'ORE REquired: ' + str(amountOre) + ' for ' + element
    return amountOre


oreReqs = 0
amount = 2600000
while oreReqs == 0:
    elementStore = {}
    elementStore['ORE'] = 1000000000000
    oreReqs = getOreRequirements('FUEL', amount)
    print 'now ' + str(amount)
    amount += 1

print 'AMOUNT POSSIBLE ' + str(amount - 2)
# print 'Ore Required: ' + str(getOreRequirements('FUEL', 460665))
# print 'Ore Consumption Map: ' + str(oreForX)
# print 'ELEMENT MAP: ' + str(elementStore)
