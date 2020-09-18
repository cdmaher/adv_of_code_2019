import sys
import copy
from sets import Set

file = open(sys.argv[1], 'r')
lines = file.readlines()

asteroidFieldInit = []
for line in lines:
    asteroidFieldInit.append(list(line.rstrip("\r\n")))


def gcd(a, b):
    if a == b:
        return a
    elif a > b:
        return gcd(a - b, b)
    elif b > a:
        return gcd(a, b - a)


def calcSightLine(asteroidField, i, j, x, y):
    count = 0
    scale = 1
    origX = x
    origY = y
    print 'Line: ' + str(x) + ' ' + str(y)
    while j + x < len(asteroidField[0]) and i + y < len(asteroidField):
        if asteroidField[i + y][j + x] == '#':
            print 'Found1: ' + str(i + y) + ' ' + str(j + x)
            count += 1
            break
        scale += 1
        x = origX * scale
        y = origY * scale
    scale = 1
    x = origX
    y = origY
    while j - x >= 0 and i - y >= 0:
        if asteroidField[i - y][j - x] == '#':
            print 'Found2: ' + str(i - y) + ' ' + str(j - x)
            count += 1
            break
        scale += 1
        x = origX * scale
        y = origY * scale
    scale = 1
    x = origX
    y = origY
    while j - x >= 0 and i + y < len(asteroidField) and y != 0 and x != 0:
        if asteroidField[i + y][j - x] == '#':
            print 'Found3: ' + str(i + y) + ' ' + str(j - x)
            count += 1
            break
        scale += 1
        x = origX * scale
        y = origY * scale
    scale = 1
    x = origX
    y = origY
    while j + x < len(asteroidField[0]) and i - y >= 0 and x != 0 and y != 0:
        if asteroidField[i - y][j + x] == '#':
            print 'Found4: ' + str(i - y) + ' ' + str(j + x)
            count += 1
            break
        scale += 1
        x = origX * scale
        y = origY * scale
    return count


def calcAsteroids(asteroidField, i, j):
    count = 0
    for y in range(0, len(asteroidField)):
        for x in range(0, len(asteroidField[y])):
            if x == 0 or y == 0:
                if x == 1 or y == 1:
                    count += calcSightLine(asteroidField, i, j, x, y)
            elif x == 1 or y == 1:
                count += calcSightLine(asteroidField, i, j, x, y)
            elif gcd(x, y) == 1:
                count += calcSightLine(asteroidField, i, j, x, y)
            # elif x % y != 0 and y % x != 0:
            #     count += calcSightLine(asteroidField, i, j, x, y)
    return count


asteroidSightMap = copy.deepcopy(asteroidFieldInit)

# The best: ((20, 19), 284)
#
bestX = 20
bestY = 19

curCounts = []


def vaporizeTopRight(asteroids, x, y, curCounts):
    scale = 1
    origX = x
    origY = y
    print 'Line: ' + str(x) + ' ' + str(y)
    while bestX + x < len(asteroids[0]) and bestY - y >= 0:
        if asteroids[bestY - y][bestX + x] == '#':
            print 'Found4: ' + str(bestY - y) + ' ' + str(bestX + x)
            curCounts.append((bestX + x, bestY - y))
            asteroids[bestY - y][bestX + x] = len(curCounts)
            break
        scale += 1
        x = origX * scale
        y = origY * scale


def vaporizeBottomRight(asteroids, x, y, curCounts):
    scale = 1
    origX = x
    origY = y
    print 'Line: ' + str(x) + ' ' + str(y)
    while bestX + x < len(asteroids[0]) and bestY + y < len(asteroids):
        if asteroids[bestY + y][bestX + x] == '#':
            print 'Found4: ' + str(bestY + y) + ' ' + str(bestX + x)
            curCounts.append((bestX + x, bestY + y))
            asteroids[bestY + y][bestX + x] = len(curCounts)
            break
        scale += 1
        x = origX * scale
        y = origY * scale


def vaporizeBottomLeft(asteroids, x, y, curCounts):
    scale = 1
    origX = x
    origY = y
    print 'Line: ' + str(x) + ' ' + str(y)
    while bestX - x >= 0 and bestY + y < len(asteroids):
        if asteroids[bestY + y][bestX - x] == '#':
            print 'Found4: ' + str(bestY + y) + ' ' + str(bestX - x)
            curCounts.append((bestX - x, bestY + y))
            asteroids[bestY + y][bestX - x] = len(curCounts)
            break
        scale += 1
        x = origX * scale
        y = origY * scale


def vaporizeTopLeft(asteroids, x, y, curCounts):
    scale = 1
    origX = x
    origY = y
    print 'Line: ' + str(x) + ' ' + str(y)
    while bestX - x >= 0 and bestY - y >= 0:
        if asteroids[bestY - y][bestX - x] == '#':
            print 'Found4: ' + str(bestY - y) + ' ' + str(bestX - x)
            curCounts.append((bestX - x, bestY - y))
            asteroids[bestY - y][bestX - x] = len(curCounts)
            break
        scale += 1
        x = origX * scale
        y = origY * scale


coords = []
for i in range(0, len(asteroidFieldInit)):
    for j in range(0, len(asteroidFieldInit[i])):
        if i == 0 or j == 0:
            if i == 1 or j == 1:
                coords.append((j, i))
        elif i == 1 or j == 1:
            coords.append((j, i))
        elif gcd(i, j) == 1:
            coords.append((j, i))

sorted_coords = sorted(
    coords,
    key=lambda coord: 9999999 if coord[1] == 0 else coord[0] * .1 / coord[1])

revSorted = sorted(
    coords,
    key=lambda coord: 9999999 if coord[1] == 0 else coord[0] * .1 / coord[1],
    reverse=True)


def fullVaporizeRotation(asteroidFieldInit, sorted_coords, revCoords,
                         curCounts):
    for i in range(0, len(sorted_coords)):
        vaporizeTopRight(asteroidFieldInit, sorted_coords[i][0],
                         sorted_coords[i][1], curCounts)

    for i in range(1, len(revSorted)):
        vaporizeBottomRight(asteroidFieldInit, revSorted[i][0],
                            revSorted[i][1], curCounts)

    for i in range(1, len(sorted_coords)):
        vaporizeBottomLeft(asteroidFieldInit, sorted_coords[i][0],
                           sorted_coords[i][1], curCounts)

    for i in range(1, len(revSorted) - 1):
        vaporizeTopLeft(asteroidFieldInit, revSorted[i][0], revSorted[i][1],
                        curCounts)


def printField(asteroids):
    for i in range(0, len(asteroids)):
        for j in range(0, len(asteroids[i])):
            print asteroids[i][j],
        print ''


prevCount = -1
while len(curCounts) != prevCount:
    prevCount = len(curCounts)
    fullVaporizeRotation(asteroidFieldInit, sorted_coords, revSorted,
                         curCounts)


def printCounts(curCounts):
    for i in range(0, len(curCounts)):
        print str(i + 1) + ': ' + str(curCounts[i])


print 'First Pass ' + str(sorted_coords)
print 'Rev ' + str(revSorted)
printField(asteroidFieldInit)
print 'Coords: '
printCounts(curCounts)

for i in range(0, len(asteroidFieldInit)):
    for j in range(0, len(asteroidFieldInit[i])):
        if asteroidFieldInit[i][j] != '.' and asteroidFieldInit[i][j] != '#' and int(
                asteroidFieldInit[i][j]) == 200:
            print '200: ' + str((j, i))
            print 'ANS: ' + str(j * 100 + i)

# Part 1
# for i in range(0, len(asteroidFieldInit)):
#     for j in range(0, len(asteroidFieldInit[i])):
#         if asteroidFieldInit[i][j] == '#':
#             numSighted = calcAsteroids(asteroidFieldInit, i, j)
#             asteroidSightMap[i][j] = str(numSighted)
#         else:
#             asteroidSightMap[i][j] = '.'

# def highestSightLine(asteroids):
#     max = 0
#     coords = (0, 0)
#     for i in range(0, len(asteroids)):
#         for j in range(0, len(asteroids[i])):
#             if asteroids[i][j] != '.' and int(asteroids[i][j]) > max:
#                 max = int(asteroids[i][j])
#                 coords = (j, i)
#     return (coords, max)

# print 'Field: '
# printField(asteroidSightMap)
# print 'The best: ' + str(highestSightLine(asteroidSightMap))
