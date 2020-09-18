import sys
import copy
import math
from functools import reduce
from sets import Set

file = open(sys.argv[1], 'r')
lines = file.readlines()

erisArea = [[['.' for i in range(5)] for j in range(5)]
            for depth in range(300)]
lineN = 0
firstArea = erisArea[150]
for line in lines:
    splitL = list(line.rstrip('\r\n'))
    splitN = 0
    for cell in splitL:
        firstArea[lineN][splitN] = cell
        splitN += 1
    lineN += 1

layouts = {}


def printArea(area):
    print ''
    for i in range(0, len(area)):
        for j in range(0, len(area[i])):
            print area[i][j],
        print ''


def printDimensionRange(dimensions, start, end):
    mid = (start + end) / 2
    for i in range(start, end + 1):
        print 'Depth ' + str(i - mid)
        printArea(dimensions[i])
        print '\n'


def numBugsAdjacent(area, pos):
    numBugs = 0
    if pos[0] - 1 >= 0 and area[pos[0] - 1][pos[1]] == '#':
        numBugs += 1
    if pos[0] + 1 < len(area) and area[pos[0] + 1][pos[1]] == '#':
        numBugs += 1
    if pos[1] + 1 < len(area[0]) and area[pos[0]][pos[1] + 1] == '#':
        numBugs += 1
    if pos[1] - 1 >= 0 and area[pos[0]][pos[1] - 1] == '#':
        numBugs += 1
    return numBugs


def runGeneration(area):
    newArea = copy.deepcopy(area)
    for i in range(0, len(area)):
        for j in range(0, len(area[0])):
            adjacent = numBugsAdjacent(area, (i, j))
            if area[i][j] == '#' and adjacent != 1:
                newArea[i][j] = '.'
            elif area[i][j] == '.' and (adjacent == 1 or adjacent == 2):
                newArea[i][j] = '#'
    return newArea


def numBugsAdjacentDimensions(dimensions, pos):
    numBugs = 0
    # if pos[1] == 0 and pos[2] == 1:
    #     print 'why ' + str(100 - pos[0])
    #     printArea(dimensions[pos[0]])
    if pos[1] - 1 == 2 and pos[2] == 2:
        for i in range(0, 5):
            numBugs += 1 if dimensions[pos[0] + 1][4][i] == '#' else 0
        # if pos[1] == 3 and pos[2] == 2:
        #     print 'shit the 1 ' + str(numBugs) + ' ' + str(
        #         dimensions[pos[0] + 1][4])
    elif pos[1] - 1 >= 0 and dimensions[pos[0]][pos[1] - 1][pos[2]] == '#':
        numBugs += 1
        # if pos[1] == 0 and pos[2] == 1:
        #     print 'shit the 2 ' + str(numBugs)
    elif pos[1] - 1 < 0 and dimensions[pos[0] - 1][1][2] == '#':
        numBugs += 1
        # if pos[1] == 0 and pos[2] == 1:
        #     print 'shit the 3 ' + str(numBugs)
    if pos[1] + 1 == 2 and pos[2] == 2:
        for i in range(0, 5):
            numBugs += 1 if dimensions[pos[0] + 1][0][i] == '#' else 0
        # if pos[1] == 1 and pos[2] == 2:
        #     print 'shit the 4 ' + str(numBugs)
    elif pos[1] + 1 < len(
            dimensions[0]) and dimensions[pos[0]][pos[1] + 1][pos[2]] == '#':
        numBugs += 1
        # if pos[1] == 0 and pos[2] == 1:
        #     print 'shit the 5 ' + str(numBugs)
    elif pos[1] + 1 >= len(
            dimensions[0]) and dimensions[pos[0] - 1][3][2] == '#':
        numBugs += 1
        # if pos[1] == 0 and pos[2] == 1:
        #     print 'shit the 6 ' + str(numBugs)
    if pos[2] - 1 == 2 and pos[1] == 2:
        for i in range(0, 5):
            numBugs += 1 if dimensions[pos[0] + 1][i][4] == '#' else 0
        # if pos[1] == 2 and pos[2] == 3:
        #     print 'shit the 7 ' + str(numBugs)
    elif pos[2] - 1 >= 0 and dimensions[pos[0]][pos[1]][pos[2] - 1] == '#':
        numBugs += 1
        # if pos[1] == 0 and pos[2] == 1:
        #     print 'shit the 8 ' + str(numBugs)
    elif pos[2] - 1 < 0 and dimensions[pos[0] - 1][2][1] == '#':
        numBugs += 1
        # if pos[1] == 0 and pos[2] == 1:
        #     print 'shit the 9 ' + str(numBugs)
    if pos[2] + 1 == 2 and pos[1] == 2:
        for i in range(0, 5):
            numBugs += 1 if dimensions[pos[0] + 1][i][0] == '#' else 0
            # if pos[1] == 0 and pos[2] == 1:
            #     print 'shit the 10 ' + str(numBugs)
    elif pos[2] + 1 < len(
            dimensions[0][0]) and dimensions[pos[0]][pos[1]][pos[2]
                                                             + 1] == '#':
        numBugs += 1
        # if pos[1] == 0 and pos[2] == 1:
        #     print 'shit the 11 ' + str(numBugs)
    elif pos[2] + 1 >= len(
            dimensions[0][0]) and dimensions[pos[0] - 1][2][3] == '#':
        numBugs += 1
        # if pos[1] == 0 and pos[2] == 1:
        #     print 'shit the 12 ' + str(numBugs)
    return numBugs


def runGenerationDimension(dimensions):
    newDims = copy.deepcopy(dimensions)
    for dim in range(1, len(dimensions) - 1):
        area = dimensions[dim]
        newArea = newDims[dim]
        for i in range(0, len(area)):
            for j in range(0, len(area[0])):
                if i == 2 and j == 2:
                    continue
                adjacent = numBugsAdjacentDimensions(dimensions, (dim, i, j))
                # if i == 3 and j == 2:
                #     print 'fuc ' + str(adjacent)
                if area[i][j] == '#' and adjacent != 1:
                    newArea[i][j] = '.'
                elif area[i][j] == '.' and (adjacent == 1 or adjacent == 2):
                    newArea[i][j] = '#'
    return newDims


def getBioRating(area):
    rating = 0
    for i in range(0, len(area)):
        for j in range(0, len(area[i])):
            if area[i][j] == '#':
                rating += pow(2, i * 5 + j)
    return rating


def countAllBugs(dimensions):
    bugs = 0
    for dim in range(0, len(dimensions)):
        for i in range(0, len(dimensions[dim])):
            for j in range(0, len(dimensions[dim][i])):
                if dimensions[dim][i][j] == '#':
                    bugs += 1
    return bugs


count = 200
minute = 0
printDimensionRange(erisArea, 145, 155)
while minute < count:
    erisArea = runGenerationDimension(erisArea)
    minute += 1

printDimensionRange(erisArea, 145, 155)
print 'CHEck 0'
printArea(erisArea[1])
print 'CHEck last'
printArea(erisArea[298])
print 'ANS: ' + str(countAllBugs(erisArea))

# count = 90000000
# minute = 0
# bioRating = getBioRating(erisArea)
# secondRating = 0
# layouts[bioRating] = 1
# printArea(erisArea)
# while minute < count:
#     erisArea = runGeneration(erisArea)
#     bioRating = getBioRating(erisArea)
#     # printArea(erisArea)
#     if bioRating in layouts:
#         secondRating = bioRating
#         break
#     layouts[bioRating] = 1
#     minute += 1
#
# print 'ANS: ' + str(secondRating)
# print 'TOOK: ' + str(minute) + ' minutes'
