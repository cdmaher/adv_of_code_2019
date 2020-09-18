import sys
import copy
import math
import time
from functools import reduce
from sets import Set

file = open(sys.argv[1], 'r')
lines = file.readlines()

start = int(round(time.time() * 1000.0))
print "Start Time =" + str(start)


class WarpPoint:
    def __init__(self, name, pointOne, isFirstOuter):
        self.name = name
        self.pointOne = pointOne
        self.pointTwo = None
        self.isFirstOuter = isFirstOuter

    def setWarpTwo(self, pointTwo):
        self.pointTwo = pointTwo

    def isOuter(self, point):
        if (self.isFirstOuter
                and point == self.pointOne) or (not self.isFirstOuter
                                                and point == self.pointTwo):
            return True
        return False

    def warp(self, start):
        if start == self.pointOne:
            return self.pointTwo
        else:
            return self.pointOne

    def __str__(self):
        fromPoint = 'OUTER ' if self.isFirstOuter else 'INNER '
        toPoint = 'INNER ' if self.isFirstOuter else 'OUTER '
        return ' Name: ' + self.name + ', from ' + fromPoint + str(
            self.pointOne) + ' to ' + toPoint + str(self.pointTwo) + '\n'

    __repr__ = __str__


def printMaze(maze):
    for i in range(0, len(maze)):
        for j in range(0, len(maze[i])):
            print maze[i][j][0],
        print ''


maze = []
mazeDict = {}

for line in lines:
    tiles = list(line.rstrip("\r\n"))
    maze.append([])
    for tile in tiles:
        maze[-1].append(tile)


def findWarpPoint(position):
    rightPos = (position[0], position[1] + 1)
    bottomPos = (position[0] + 1, position[1])
    bottomWarp = (position[0] + 2, position[1])
    topWarp = (position[0] - 1, position[1])
    leftWarp = (position[0], position[1] - 1)
    rightWarp = (position[0], position[1] + 2)
    if position[0] + 1 >= len(maze) or position[1] + 1 >= len(maze[0]):
        return None

    newWarpPoint = None
    hasFoundFirst = False
    name = ''
    isOuter = False
    if ord(maze[rightPos[0]][rightPos[1]]) >= 65 and ord(
            maze[rightPos[0]][rightPos[1]]):
        name = maze[position[0]][position[1]] + maze[rightPos[0]][rightPos[1]]
        hasFoundFirst = name in mazeDict
        if position[1] + 2 < len(
                maze[0]) and maze[rightWarp[0]][rightWarp[1]] == '.':
            newWarpPoint = rightWarp
            if position[1] == 0:
                isOuter = True
        elif position[1] - 1 > 0 and maze[leftWarp[0]][leftWarp[1]] == '.':
            newWarpPoint = leftWarp
            if position[1] + 2 == len(maze[0]):
                isOuter = True
    elif ord(maze[bottomPos[0]][bottomPos[1]]) >= 65 and ord(
            maze[bottomPos[0]][bottomPos[1]]):
        name = maze[position[0]][position[1]] + maze[bottomPos[0]][bottomPos[1]]
        hasFoundFirst = name in mazeDict
        if position[0] + 2 < len(
                maze) and maze[bottomWarp[0]][bottomWarp[1]] == '.':
            newWarpPoint = bottomWarp
            print 'found ' + str(newWarpPoint) + ' ' + name + ' ' + str(
                position)
            if position[0] == 0:
                isOuter = True
        elif position[0] - 1 > 0 and maze[topWarp[0]][topWarp[1]] == '.':
            newWarpPoint = topWarp
            if position[0] + 2 == len(maze):
                isOuter = True
    if (not newWarpPoint is None) and hasFoundFirst:
        warp = mazeDict[name]
        warp.setWarpTwo(newWarpPoint)
        return warp
    elif not newWarpPoint is None:
        warp = WarpPoint(name, newWarpPoint, isOuter)
        mazeDict[name] = warp
        return warp
    return None


def getWarpPoint(position):
    topPos = (position[0] - 1, position[1])
    leftPos = (position[0], position[1] - 1)
    rightPos = (position[0], position[1] + 1)
    bottomPos = (position[0] + 1, position[1])
    if position[0] - 1 < 0 or position[1] - 1 < 0:
        return None
    if ord(maze[leftPos[0]][leftPos[1]][0]) >= 65 and ord(
            maze[leftPos[0]][leftPos[1]][0]):
        return maze[leftPos[0]][leftPos[1]][0] + maze[position[0]][position[1]][0]
    elif ord(maze[topPos[0]][topPos[1]][0]) >= 65 and ord(
            maze[topPos[0]][topPos[1]][0]):
        return maze[topPos[0]][topPos[1]][0] + maze[position[0]][position[1]][0]
    elif ord(maze[bottomPos[0]][bottomPos[1]][0]) >= 65 and ord(
            maze[bottomPos[0]][bottomPos[1]][0]):
        return maze[position[0]][position[1]][0] + maze[bottomPos[0]][bottomPos[1]][0]
    elif ord(maze[rightPos[0]][rightPos[1]][0]) >= 65 and ord(
            maze[rightPos[0]][rightPos[1]][0]):
        return maze[position[0]][position[1]][0] + maze[rightPos[0]][rightPos[1]][0]


def getNextPositions(map, pos):
    nextPositions = []
    if pos[0] + 1 < len(map) and map[pos[0] + 1][pos[1]][0] != '#':
        nextPositions.append((pos[0] + 1, pos[1]))
    if pos[0] - 1 >= 0 and map[pos[0] - 1][pos[1]][0] != '#':
        nextPositions.append((pos[0] - 1, pos[1]))
    if pos[1] + 1 < len(map[0]) and map[pos[0]][pos[1] + 1][0] != '#':
        nextPositions.append((pos[0], pos[1] + 1))
    if pos[1] - 1 >= 0 and map[pos[0]][pos[1] - 1][0] != '#':
        nextPositions.append((pos[0], pos[1] - 1))
    return nextPositions


def pathToGoalBFS(maze, pos, goal):
    found = False
    path = 0
    curPosLevel = (pos, 0)
    mazeLevels = []
    maxLevel = 100
    mazeLevels.append(copy.deepcopy(maze))
    posToVisit = []
    mazeLevels[0][pos[0]][pos[1]] = (maze[pos[0]][pos[1]][0], 0)
    while not found:
        (curPos, curLevel) = curPosLevel
        potPos = getNextPositions(maze, curPos)
        prevLevel = curLevel
        for nextPos in potPos:
            (tile, pathLength) = mazeLevels[curLevel][curPos[0]][curPos[1]]
            if ord(maze[nextPos[0]][nextPos[1]][0]) >= 65 and ord(
                    maze[nextPos[0]][nextPos[1]][0]) <= 90:
                warpPoint = getWarpPoint(nextPos)
                isOuterWarpPoint = mazeDict[warpPoint].isOuter(curPos)
                if warpPoint == goal and curLevel == 0:
                    return pathLength
                else:
                    warpPos = mazeDict[warpPoint].warp(curPos)
                    if not warpPos is None:
                        if isOuterWarpPoint and curLevel > 0:
                            # print 'Warpin up ' + warpPoint + str(
                            #     curPos) + ' to ' + str(
                            #         warpPos) + ' from level ' + str(
                            #             curLevel) + ' ' + str(pathLength)
                            curLevel -= 1
                            nextPos = warpPos
                        elif not isOuterWarpPoint and curLevel < maxLevel:
                            # print 'Warpin down ' + warpPoint + str(
                            #     curPos) + ' to ' + str(
                            #         warpPos) + ' from level ' + str(
                            #             curLevel) + ' ' + str(pathLength)
                            curLevel += 1
                            if len(mazeLevels) == curLevel:
                                print 'NEW CUR: ' + str(curLevel)
                                mazeLevels.append(copy.deepcopy(maze))
                            nextPos = warpPos
            if maze[nextPos[0]][nextPos[1]][0] == '.' and mazeLevels[curLevel][nextPos[0]][nextPos[1]][1] == -1:
                # print 'LEVEL: ' + str(curLevel)
                # print 'NEW LENGTH: ' + str(pathLength + 1)
                # print 'Next POS to SET ' + str(nextPos)
                # print 'SETTING FROM: ' + str(curPosLevel) + '\n'
                mazeLevels[curLevel][nextPos[0]][nextPos[1]] = (
                    maze[nextPos[0]][nextPos[1]][0], pathLength + 1)
                posToVisit.append((nextPos, curLevel))
            curLevel = prevLevel
        if len(posToVisit) == 0:
            return None
        curPosLevel = posToVisit[0]
        posToVisit = posToVisit[1:]


for i in range(0, len(maze)):
    for j in range(0, len(maze[i])):
        if ord(maze[i][j]) >= 65 and ord(maze[i][j]) <= 90:
            findWarpPoint((i, j))

for i in range(0, len(maze)):
    for j in range(0, len(maze[i])):
        maze[i][j] = (maze[i][j], -1)

print 'WARPS: \n' + str(mazeDict)

printMaze(maze)

end = int(round(time.time() * 1000.0))
print 'DO BFS: ' + str(end)

print 'SHORTEST: ' + str(pathToGoalBFS(maze, mazeDict['AA'].pointOne, 'ZZ'))

foundTime = int(round(time.time() * 1000.0))
print 'FOUND IN ' + str(foundTime - start)
