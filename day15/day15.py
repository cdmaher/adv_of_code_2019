import sys
import copy
from sets import Set

file = open(sys.argv[1], 'r')

programInit = file.readline().rstrip("\n\r").split(',')


def runProgram(program, inputSignals, curIns, relativeBase):
    i = curIns
    outputs = []
    inputSignalCount = 0
    halted = False
    while i < len(program):
        opcode = int(program[i]) % 100
        if opcode == 99:
            halted = True
            break
        mode1 = (int(program[i]) % 1000) / 100
        mode2 = (int(program[i]) % 10000) / 1000
        mode3 = int(program[i]) / 10000
        firstParam = 0
        if mode1 == 0:
            firstParam = int(program[int(program[i + 1])])
        if mode1 == 1:
            firstParam = int(program[i + 1])
        elif mode1 == 2:
            firstParam = int(program[int(program[i + 1]) + relativeBase])
        secondParam = 0
        if opcode == 1 or opcode == 2 or opcode == 5 or opcode == 6 or opcode == 7 or opcode == 8:
            if mode2 == 0:
                secondParam = int(program[int(program[i + 2])])
            if mode2 == 1:
                secondParam = int(program[i + 2])
            elif mode2 == 2:
                secondParam = int(program[int(program[i + 2]) + relativeBase])
        thirdParam = 0
        if opcode == 1 or opcode == 2 or opcode == 7 or opcode == 8:
            thirdParam = int(program[i + 3])
            if mode3 == 2:
                thirdParam = int(program[i + 3]) + relativeBase

        if opcode == 1:
            program[thirdParam] = firstParam + secondParam
            i += 4
        elif opcode == 2:
            program[thirdParam] = firstParam * secondParam
            i += 4
        elif opcode == 3:
            toSet = inputSignals[inputSignalCount]
            inputSignalCount += 1
            program[int(program[i + 1])
                    + (relativeBase if mode1 == 2 else 0)] = toSet
            i += 2
        elif opcode == 5:
            if firstParam != 0:
                i = secondParam
            else:
                i += 3
        elif opcode == 6:
            if firstParam == 0:
                i = secondParam
            else:
                i += 3
        elif opcode == 7:
            if firstParam < secondParam:
                program[thirdParam] = 1
            else:
                program[thirdParam] = 0
            i += 4
        elif opcode == 8:
            if firstParam == secondParam:
                program[thirdParam] = 1
            else:
                program[thirdParam] = 0
            i += 4
        elif opcode == 4:
            outputs.append(firstParam)
            i += 2
            return (program, outputs, False, i, relativeBase)
        elif opcode == 9:
            relativeBase += firstParam
            i += 2
        else:
            print 'NOPE'
            exit(1)
    return (program, outputs, halted, i, relativeBase)


program = programInit + ([0] * 2048)

dirs = [2, 4, 1, 3]


def printDroidArea(map, area, droidPos):
    for i in range(0, len(area)):
        for j in range(0, len(area[i])):
            if (i, j) in map:
                if i == 25 and j == 25:
                    print 'X',
                elif i == droidPos[0] and j == droidPos[1]:
                    print 'D',
                elif map[i, j][0] == 1:
                    if map[i, j][1] == 0:
                        print '.',
                    elif map[i, j][1] == 1:
                        print 'o',
                elif map[i, j][0] == 0:
                    print '#',
                elif map[i, j][0] == 2:
                    print 'O',
            else:
                print ' ',
        print ''


def markArea(area, dir, pos, output):
    posToMark = getPosFromDir(dir, pos)
    curPosInfo = area[(pos[0], pos[1])]
    area[(pos[0], pos[1])] = (curPosInfo[0], curPosInfo[1] + 1)
    if posToMark in area:
        area[(posToMark[0],
              posToMark[1])] = (output,
                                area[(posToMark[0], posToMark[1])][1] + 1)
    else:
        area[(posToMark[0], posToMark[1])] = (output, 0)


def getPosFromDir(dir, pos):
    if dir == 1:
        return (pos[0] - 1, pos[1])
    elif dir == 2:
        return (pos[0] + 1, pos[1])
    elif dir == 3:
        return (pos[0], pos[1] - 1)
    elif dir == 4:
        return (pos[0], pos[1] + 1)


def moveDroid(area, dir, pos, output):
    if output == 1 or output == 2:
        pos = getPosFromDir(dir, pos)
    for i in dirs:
        potPos = getPosFromDir(i, pos)
        if potPos not in area:
            return (pos, i)
    minToVisit = 999999999
    bestDir = 0
    for i in dirs:
        potPos = getPosFromDir(i, pos)
        if area[(potPos[0], potPos[1])][0] == 1:
            if area[(potPos[0], potPos[1])][1] < minToVisit:
                minToVisit = area[(potPos[0], potPos[1])][1]
                bestDir = i
    return (pos, bestDir)


areaMap = {}
bigGrid = [[0] * 50 for i in range(50)]
droidPos = (25, 25)
areaMap[droidPos[0], droidPos[1]] = (-1, 0)

droidRightTest = 1000
droidDownTest = 1000
droidUpTest = -500
droidLeftTest = -500


def moveDroidTest(curPos, dir):
    if dir == 4 and curPos[1] < droidRightTest:
        return ((curPos[0], curPos[1] + 1), 4)
    elif dir == 4:
        return ((curPos[0] + 1, curPos[1]), 3)
    elif dir == 3 and curPos[1] > 0:
        return ((curPos[0], curPos[1] - 1), 3)
    elif dir == 3:
        return ((curPos[0] + 1, curPos[1]), 4)


output = 0
halted = False
curIns = 0
relativeBase = 0
curDir = 3
count = 0
pathLen = 0
while count < 10000:
    (program, outputs, halted, i, relativeBase) = runProgram(
        program, [curDir], curIns, relativeBase)
    if halted:
        break
    # if count % 100 == 0:
    # print 'tf ' + str(droidPos) + ' ' + str(output)
    # printDroidArea(droidArea, droidPos)
    if False:
        # printDroidArea(droidArea, droidPos)
        print 'pos out o ragne ' + str(count)
        print 'tf ' + str(droidPos) + ' ' + str(output)
        exit(1)
    output = outputs[0]
    markArea(areaMap, curDir, droidPos, output)
    (droidPos, curDir) = moveDroid(areaMap, curDir, droidPos, output)
    if curDir == 0:
        print 'FUCK '
        exit(1)
    count += 1

for cell in areaMap:
    areaMap[cell] = (areaMap[cell][0], -1)

def findShortestPath(areaMap, pos):
    nextSteps = []
    for i in dirs:
        nextSteps.append(getPosFromDir(i, pos))

    shortest = 99999999
    areaMap[pos] = (areaMap[pos][0], shortest)
    for step in nextSteps:
        if step in areaMap and areaMap[step][0] == 2:
            areaMap[pos] = (areaMap[pos][0], 1)
            print 'found ' + str(pos)
            return 1
        elif step in areaMap and areaMap[step][0] == 1 and areaMap[step][1] == -1:
            # print ' bleh'
            shortestStep = findShortestPath(areaMap, step)
            if shortestStep < shortest:
                shortest = shortestStep
    areaMap[pos] = (areaMap[pos][0], shortest + 1)
    return shortest + 1

spaceCount = 0
newOxToSpread = []
for cell in areaMap:
    if areaMap[cell][0] == 2:
        areaMap[cell] = (areaMap[cell][0], 1)
        newOxToSpread.append(cell)
    elif areaMap[cell][0] == 1:
        spaceCount += 1
        areaMap[cell] = (areaMap[cell][0], 0)

print 'Space to Fill ' + str(spaceCount)

filledOx = 0
minutes = 0
while filledOx < spaceCount:
    oxToSpread = copy.deepcopy(newOxToSpread)
    newOxToSpread = []
    for oxSpace in oxToSpread:
        nextSteps = []
        for i in dirs:
            nextSteps.append(getPosFromDir(i, oxSpace))
        for step in nextSteps:
            if step in areaMap and areaMap[step][0] == 1 and areaMap[step][1] == 0:
                filledOx += 1
                areaMap[step] = (areaMap[step][0], 1)
                newOxToSpread.append(step)
    minutes += 1

print 'time to Fill ' + str(minutes)
printDroidArea(areaMap, bigGrid, droidPos)

# Part 1
# print 'Result: ' + str(halted) + ' ' + str(output)
# # answer = findShortestPath(areaMap, (25, 25))
# printDroidArea(areaMap, bigGrid, droidPos)
# print 'ANSWER ' + str(answer)
