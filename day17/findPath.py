import sys
import copy
import math
from sets import Set

file = open(sys.argv[1], 'r')
lines = file.readlines()

scaffoldView = []
for line in lines:
    scaffLine = list(line.strip("\r\n").replace(' ', ''))
    scaffoldView.append([])
    for cell in scaffLine:
        scaffoldView[-1].append(cell)

start = (0, 0)
curDir = 1
for i in range(0, len(scaffoldView)):
    for j in range(0, len(scaffoldView[i])):
        if scaffoldView[i][j] == '<':
            curDir = 3
            start = (j, i)
        elif scaffoldView[i][j] == 'v':
            curDir = 2
            start = (j, i)
        elif scaffoldView[i][j] == '>':
            curDir = 4
            start = (j, i)
        elif scaffoldView[i][j] == '^':
            curDir = 1
            start = (i, j)


def oppDir(dir):
    if dir == 1:
        return 2
    elif dir == 2:
        return 1
    elif dir == 3:
        return 4
    elif dir == 4:
        return 3


def getPosFromDir(dir, pos):
    if dir == 1:
        return (pos[0] - 1, pos[1])
    elif dir == 2:
        return (pos[0] + 1, pos[1])
    elif dir == 3:
        return (pos[0], pos[1] - 1)
    elif dir == 4:
        return (pos[0], pos[1] + 1)


def hasNextSpot(view, pos):
    if pos[0] < 0 or pos[1] < 0 or pos[0] > len(view) - 1 or pos[1] > len(
            view[0]) - 1:
        return False
    return view[pos[0]][pos[1]] == '#'


def findTurn(view, curDir, curPos):
    oppD = oppDir(curDir)
    for i in range(1, 5):
        potPos = getPosFromDir(i, curPos)
        if i != oppD and hasNextSpot(view, potPos):
            if i == 1:
                if curDir == 3:
                    return ('R', i)
                elif curDir == 4:
                    return ('L', i)
            elif i == 2:
                if curDir == 3:
                    return ('L', i)
                elif curDir == 4:
                    return ('R', i)
            elif i == 3:
                if curDir == 1:
                    return ('L', i)
                elif curDir == 2:
                    return ('R', i)
            elif i == 4:
                if curDir == 1:
                    return ('R', i)
                elif curDir == 2:
                    return ('L', i)
    return ('', 0)


def advanceRobot(view, curDir, curPos):
    advanced = 0
    nextSpot = getPosFromDir(curDir, curPos)
    while hasNextSpot(view, nextSpot):
        curPos = nextSpot
        nextSpot = getPosFromDir(curDir, curPos)
        advanced += 1
    return (advanced, curPos)


path = ''
(curTurn, curDir) = findTurn(scaffoldView, curDir, start)
curPos = start
while curTurn != '':
    path += curTurn + ','
    (advanced, curPos) = advanceRobot(scaffoldView, curDir, curPos)
    path += str(advanced) + ','
    (curTurn, curDir) = findTurn(scaffoldView, curDir, curPos)

print 'PATH: ' + str(path)
