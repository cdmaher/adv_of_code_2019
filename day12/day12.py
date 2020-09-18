import sys
import copy
from sets import Set


class Moon:
    def __init__(self, pos):
        self.initPos = pos
        self.initVel = (0, 0, 0)
        self.pos = pos
        self.vel = (0, 0, 0)

    def applyGravity(self, otherMoons):
        for moon in otherMoons:
            newX = self.vel[0] + (1 if self.pos[0] < moon.pos[0] else 0
                                  if self.pos[0] == moon.pos[0] else -1)
            newY = self.vel[1] + (1 if self.pos[1] < moon.pos[1] else 0
                                  if self.pos[1] == moon.pos[1] else -1)
            newZ = self.vel[2] + (1 if self.pos[2] < moon.pos[2] else 0
                                  if self.pos[2] == moon.pos[2] else -1)
            self.vel = (newX, newY, newZ)

    def applyVelocity(self):
        self.pos = (
            self.pos[0] + self.vel[0],
            self.pos[1] + self.vel[1],
            self.pos[2] + self.vel[2],
        )

    def calcEnergy(self):
        pot = abs(self.pos[0]) + abs(self.pos[1]) + abs(self.pos[2])
        kin = abs(self.vel[0]) + abs(self.vel[1]) + abs(self.vel[2])
        return pot * kin

    def equalsInitPosX(self):
        return self.pos[0] == self.initPos[0] and self.vel[0] == self.initVel[0]

    def equalsInitPosY(self):
        return self.pos[1] == self.initPos[1] and self.vel[1] == self.initVel[1]

    def equalsInitPosZ(self):
        return self.pos[2] == self.initPos[2] and self.vel[2] == self.initVel[2]

    def __str__(self):
        return 'pos=<x= ' + str(self.pos[0]) + ', y= ' + str(
            self.pos[1]) + ', z= ' + str(self.pos[2]) + '>, vel=<x= ' + str(
                self.vel[0]) + ', y= ' + str(self.vel[1]) + ', z= ' + str(
                    self.vel[2]) + '>'

    __repr__ = __str__


def printMoons(moons):
    for moon in moons:
        print str(moon)


file = open(sys.argv[1], 'r')
lines = file.readlines()

jupiterMoons = []
for line in lines:
    splitLine = line.replace(' ', '').strip("\r\n<>").split(',')
    jupiterMoons.append(
        Moon((
            int(splitLine[0][2:]),
            int(splitLine[1][2:]),
            int(splitLine[2][2:]),
        )))


def applyTimeStep(jupiterMoons):
    for i in range(0, len(jupiterMoons)):
        jupiterMoons[i].applyGravity(jupiterMoons)
    for moon in jupiterMoons:
        moon.applyVelocity()


# part 1
# stepsToRun = 1000
# for i in range(0, stepsToRun):
#     applyTimeStep(jupiterMoons)
# totalEnergy = reduce(
#     (lambda total, moon: total + moon.calcEnergy()),
#     jupiterMoons,
#     0,
# )
#
# printMoons(jupiterMoons)
# print 'en: ' + str(totalEnergy)

def gcd(a, b):
    if a == b:
        return a
    elif a > b:
        return gcd(a - b, b)
    elif b > a:
        return gcd(a, b - a)

def lcm(a, b):
    return (a * b) / gcd(a, b)

count = 0
hasInitX = False
hasInitY = False
hasInitZ = False
jupiterMoonsX = copy.deepcopy(jupiterMoons)
while not hasInitX:
    applyTimeStep(jupiterMoonsX)
    hasInitX = reduce(
        (lambda hasInitX, moon: hasInitX and moon.equalsInitPosX()),
        jupiterMoonsX,
        True,
    )
    count += 1

printMoons(jupiterMoonsX)

print 'Total Steps to RepeatX: ' + str(count)

countX = count
count = 0
jupiterMoonsY = copy.deepcopy(jupiterMoons)

while not hasInitY:
    applyTimeStep(jupiterMoonsY)
    hasInitY = reduce(
        (lambda hasInitY, moon: hasInitY and moon.equalsInitPosY()),
        jupiterMoonsY,
        True,
    )
    count += 1

printMoons(jupiterMoonsY)

print 'Total Steps to RepeatY: ' + str(count)

countY = count
count = 0
jupiterMoonsZ = copy.deepcopy(jupiterMoons)
while not hasInitZ:
    applyTimeStep(jupiterMoonsZ)
    hasInitZ = reduce(
        (lambda hasInitZ, moon: hasInitZ and moon.equalsInitPosZ()),
        jupiterMoonsZ,
        True,
    )
    count += 1

printMoons(jupiterMoonsZ)

print 'Total Steps to RepeatZ: ' + str(count)
countZ = count

# print 'First Repeat: ' + str(lcm(lcm(countX, countY), countZ))
