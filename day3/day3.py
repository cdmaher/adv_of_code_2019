import sys
from sets import Set

file = open(sys.argv[1], 'r')

grid = [[('', 0) for x in range(20000)] for y in range(20000)]

firstWire = file.readline().split(',')
secondWire = file.readline().split(',')


def manhattan(point):
    return abs(point[0] - 10000) + abs(point[1] - 10000)


matches = []


def traceWireInGrid(wire, color):
    curPosx, curPosy = (10000, 10000)
    traveled = 0
    for i in range(0, len(wire)):
        curLen = wire[i]
        curDir = curLen[0]
        curDist = int(curLen[1:])
        if curDir == 'D':
            for j in range(0, curDist):
                if not color in grid[curPosx + 1][curPosy][0]:
                    grid[curPosx + 1][curPosy] = (
                        grid[curPosx + 1][curPosy][0] + color,
                        grid[curPosx + 1][curPosy][1] + traveled + j + 1)
                    if len(grid[curPosx + 1][curPosy][0]) == 2:
                        matches.append((curPosx + 1, curPosy,
                                        grid[curPosx + 1][curPosy][1]))
                curPosx += 1
        elif curDir == 'R':
            for j in range(0, curDist):
                # print 'hi ' + str(curPosx) + ' ' + str(curPosy) + ' ' + curLen
                if not color in grid[curPosx][curPosy + 1][0]:
                    grid[curPosx][curPosy + 1] = (
                        grid[curPosx][curPosy + 1][0] + color,
                        grid[curPosx][curPosy + 1][1] + traveled + j + 1)
                    if len(grid[curPosx][curPosy + 1][0]) == 2:
                        matches.append((curPosx, curPosy + 1,
                                        grid[curPosx][curPosy + 1][1]))
                curPosy += 1
        elif curDir == 'U':
            for j in range(0, curDist):
                if not color in grid[curPosx - 1][curPosy][0]:
                    grid[curPosx - 1][curPosy] = (
                        grid[curPosx - 1][curPosy][0] + color,
                        grid[curPosx - 1][curPosy][1] + traveled + j + 1)
                    if len(grid[curPosx - 1][curPosy][0]) == 2:
                        matches.append((curPosx - 1, curPosy,
                                        grid[curPosx - 1][curPosy][1]))
                curPosx -= 1
        elif curDir == 'L':
            for j in range(0, curDist):
                if not color in grid[curPosx][curPosy - 1][0]:
                    grid[curPosx][curPosy - 1] = (
                        grid[curPosx][curPosy - 1][0] + color,
                        grid[curPosx][curPosy - 1][1] + traveled + j + 1)
                    if len(grid[curPosx][curPosy - 1][0]) == 2:
                        matches.append((curPosx, curPosy - 1,
                                        grid[curPosx][curPosy - 1][1]))
                curPosy -= 1
        traveled += curDist


traceWireInGrid(firstWire, 'a')
traceWireInGrid(secondWire, 'b')

print 'how many? ' + str(len(matches))
print 'matches ' + str(matches)
minMan = 100000090
best = (0, 0)
fastest = 2349284
for k in range(0, len(matches)):
    if manhattan(matches[k]) < minMan:
        best = matches[k]
        minMan = manhattan(matches[k])
    if matches[k][2] < fastest:
        fastest = matches[k][2]

print 'the nearest ' + str(best) + ' ' + str(minMan)
print 'the fastest ' + str(fastest)

# for x in range(0, len(grid)):
#     print str(grid[x])
