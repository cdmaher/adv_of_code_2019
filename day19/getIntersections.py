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


def isIntersection(view, x, y):
    if x < 0 or y < 0 or y >= len(view) - 1 or x >= len(view[0]) - 1:
        return False
    if view[y +
            1][x] == '#' and view[y][x +
                                     1] == '#' and view[y -
                                                        1][x] == '#' and view[y][x
                                                                                 -
                                                                                 1] == '#':
        return True
    return False


alignmentSum = 0
for i in range(0, len(scaffoldView)):
    for j in range(0, len(scaffoldView[i])):
        if scaffoldView[i][j] == '#' and isIntersection(scaffoldView, j, i):
            alignmentSum += i * j

print 'Alignment Sum ' + str(alignmentSum)
