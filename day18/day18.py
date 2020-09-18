import sys
import copy
import math
import string
from functools import reduce
from sets import Set

file = open(sys.argv[1], 'r')
lines = file.readlines()

areaMap = []
startPos = []
keys = {}
keyLocs = {}
doors = {}
for line in lines:
    areaMap.append([])
    cells = list(line.rstrip("\r\n"))
    for cell in cells:
        if cell == '@':
            startPos.append((len(areaMap) - 1, len(areaMap[-1])))
        elif ord(cell) >= 97 and ord(cell) <= 122:
            keys[cell] = False
            keyLocs[cell] = (len(areaMap) - 1, len(areaMap[-1]))
        elif ord(cell) >= 65 and ord(cell) <= 90:
            doors[cell] = False
        areaMap[-1].append((cell, -1))


def printAreaMap(map):
    for i in range(0, len(map)):
        for j in range(0, len(map[i])):
            print map[i][j][0],
        print ''


def isPassable(map, pos, keys, doors, ignoreDoors=False):
    if map[pos[0]][pos[1]][0] == '#':
        return False
    if map[pos[0]][pos[1]][0] == '.':
        return True
    if not ignoreDoors and map[pos[0]][pos[1]][0] in doors and not (
            string.lower(map[pos[0]][pos[1]][0]) in keys
            and keys[string.lower(map[pos[0]][pos[1]][0])]):
        return False
    return True


pathLengths = {}
memoLengths = {}


def getNextPositions(map, pos, keys, doors, ignoreDoors=False):
    nextPositions = []
    if pos[0] + 1 < len(map) and isPassable(map, (pos[0] + 1, pos[1]), keys,
                                            doors, ignoreDoors):
        nextPositions.append((pos[0] + 1, pos[1]))
    if pos[0] - 1 >= 0 and isPassable(map, (pos[0] - 1, pos[1]), keys, doors,
                                      ignoreDoors):
        nextPositions.append((pos[0] - 1, pos[1]))
    if pos[1] + 1 < len(map[0]) and isPassable(map, (pos[0], pos[1] + 1), keys,
                                               doors, ignoreDoors):
        nextPositions.append((pos[0], pos[1] + 1))
    if pos[1] - 1 >= 0 and isPassable(map, (pos[0], pos[1] - 1), keys, doors,
                                      ignoreDoors):
        nextPositions.append((pos[0], pos[1] - 1))
    return nextPositions


def setKeys(keys):
    keySet = keys.keys()
    return set([x for x in keySet if keys[x]])


def getMemoKey(keys, pos):
    keysObtained = dict(filter(lambda elem: elem[1], keys.items()))
    keySet = set(keysObtained.keys())
    keyOrdered = ''
    for key in keySet:
        keyOrdered += key
    return (keyOrdered, (pos[0], pos[1], pos[2], pos[3]))


def pathToGoalBFS(map, pos, keys, doors, goal):
    found = False
    path = 0
    posToVisit = []
    curPos = pos
    map[curPos[0]][curPos[1]] = (map[curPos[0]][curPos[1]][0], 0, set())
    while not found:
        potPos = getNextPositions(map, curPos, keys, doors, True)
        for nextPos in potPos:
            (key, pathLength, keysNeeded) = map[curPos[0]][curPos[1]]
            if map[nextPos[0]][nextPos[1]][0] == goal:
                return (pathLength + 1, keysNeeded)
            elif map[nextPos[0]][nextPos[1]][1] == -1:
                keysForNextPos = copy.deepcopy(keysNeeded)
                if map[nextPos[0]][nextPos[1]][0] in doors:
                    keysForNextPos.add(
                        string.lower(map[nextPos[0]][nextPos[1]][0]))
                map[nextPos[0]][nextPos[1]] = (map[nextPos[0]][nextPos[1]][0],
                                               pathLength + 1, keysForNextPos)
                posToVisit.append(nextPos)
        if len(posToVisit) == 0:
            return (None, set())
        curPos = posToVisit[0]
        posToVisit = posToVisit[1:]


printAreaMap(areaMap)
print 'start ' + str(startPos)
print 'keys ' + str(keys)
print 'doors ' + str(doors)


def printPaths(map, paths):
    for p in paths:
        print str(map[p[0]][p[1]][0]) + ': ' + str(paths[p])


def initialCalculation(map, keys, doors):
    for pos in startPos:
        for k in keys:
            (keyPathLen, keysNeeded) = pathToGoalBFS(
                copy.deepcopy(areaMap), pos, keys, doors, k)
            if keyPathLen != None:
                pathLengths[(pos, keyLocs[k])] = (keyPathLen, keysNeeded)
    for k in keys:
        for kGoal in keys:
            if k != kGoal:
                (keyPathLen, keysNeeded) = pathToGoalBFS(
                    copy.deepcopy(areaMap), keyLocs[k], keys, doors, kGoal)
                if keyPathLen != None:
                    pathLengths[(keyLocs[k],
                                 keyLocs[kGoal])] = (keyPathLen,
                                                     keysNeeded.difference(
                                                         set([k])))


def findPathsToKeys(posts, keys, doors):
    shortestPathLen = 9999
    paths = {}
    memoKey = getMemoKey(keys, posts)
    if memoKey in memoLengths:
        return memoLengths[memoKey]
    for k in keys:
        if not keys[k]:
            for i in range(0, len(posts)):
                if (posts[i], keyLocs[k]) in pathLengths:
                    (lenToKeys, needKeys) = pathLengths[(posts[i], keyLocs[k])]
                    if not lenToKeys is None and needKeys.issubset(
                            setKeys(keys)):
                        paths[k] = (lenToKeys, needKeys, i)
    for key in paths:
        newKeys = copy.deepcopy(keys)
        newKeys[key] = True
        (lenToKeys, needKeys, i) = paths[key]
        if any(not keyFound for keyFound in newKeys.itervalues()):
            newPosts = list(posts)
            newPosts[i] = keyLocs[key]
            pathToKey = findPathsToKeys(tuple(newPosts), newKeys, doors)
            lenToKeys += pathToKey
        if lenToKeys < shortestPathLen:
            shortestPathLen = lenToKeys
    memoLengths[getMemoKey(keys, posts)] = shortestPathLen
    return shortestPathLen


initialCalculation(copy.deepcopy(areaMap), keys, doors)

print "MEMO: " + str(pathLengths)
print "MEMO length: " + str(len(pathLengths))
totalPath = findPathsToKeys(
    (startPos[0], startPos[1], startPos[2], startPos[3]), keys, doors)

print 'Shortest: ' + str(totalPath)
# print "MEMO KEYS: " + str(memoLengths)

# print 'Path Lengths: ' + str(pathLengths)
