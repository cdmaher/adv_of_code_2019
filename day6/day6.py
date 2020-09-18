import sys
from sets import Set


class Orbiter:
    def __init__(self, name):
        self.name = name
        self.orbiters = []
        self.orbiting = None
        self.visited = False
        self.minSantaPath = 10000

    def addOrbiting(self, orbiting):
        self.orbiting = orbiting

    def addOrbiter(self, newOrbiter):
        self.orbiters.append(newOrbiter)

    def countOrbits(self):
        totalOrbits = 0
        for i in range(0, len(self.orbiters)):
            totalOrbits += 1 + self.orbiters[i].countOrbits()
        return totalOrbits

    def printMinToSanta(self):
        print 'MIN: ' + self.name + ' ' + str(self.minSantaPath)

    def __str__(self):
        return self.name + '-' + str(self.orbiters)

    __repr__ = __str__


file = open(sys.argv[1], 'r')

objNames = {}

orbits = file.readlines()

for orbit in orbits:
    masses = orbit.rstrip("\r\n").split(")")
    if not masses[1] in objNames:
        objNames[masses[1]] = Orbiter(masses[1])
    if not masses[0] in objNames:
        objNames[masses[0]] = Orbiter(masses[0])
    objNames[masses[0]].addOrbiter(objNames[masses[1]])
    objNames[masses[1]].addOrbiting(objNames[masses[0]])

# print 'OUT: ' + str(objNames['COM'])
allOrbits = 0

# PART 1
# for obj in objNames:
#     allOrbits += objNames[obj].countOrbits()


def minPathToSanta(rootObj):
    if rootObj is None:
        return 35353535345
    rootObj.visited = True
    # print 'huh ' + rootObj.name
    yourOrbiting = rootObj.orbiting
    if objNames['SAN'] in rootObj.orbiters:
        rootObj.minSantaPath = 0
        return 0
    else:
        toVisit = [9999]
        if not yourOrbiting is None and not yourOrbiting.visited:
            toVisit.append(minPathToSanta(yourOrbiting))
        # print 'sorry what ' + rootObj.name + ' ' + str(rootObj.orbiters)
        for i in range(0, len(rootObj.orbiters)):
            # print 'ffs ' + rootObj.name + ' ' + str(rootObj.orbiters[i])
            if not rootObj.orbiters[i].visited:
                toVisit.append(minPathToSanta(rootObj.orbiters[i]))
        rootObj.minSantaPath = 1 + min(toVisit)
        return 1 + min(toVisit)


rootYou = objNames['YOU']

for obj in objNames:
    objNames[obj].printMinToSanta()
print 'MIN Path: ' + str(minPathToSanta(rootYou.orbiting))
