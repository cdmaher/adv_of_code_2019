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


def printGrid(grid):
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            print grid[i][j],
        print ''


program = programInit + ([0] * 4096)

gridHeight = 200
gridWidth = 200
offSetX = 920
offSetY = 1140
grid = [[''] * gridWidth for i in range(gridHeight)]
curIns = 0
relativeBase = 0
beamAffected = 0
for i in range(0, gridHeight):
    for j in range(0, gridWidth):
        (newprogram, outputs, halted, curIns, relativeBase) = runProgram(
            copy.deepcopy(program), [j + offSetX, i + offSetY], 0, 0)
        if outputs[0] == 1:
            grid[i][j] = '#'
            beamAffected += 1
        elif outputs[0] == 0:
            grid[i][j] = '.'

print 'done with ship!'


def findShip(grid):
    for i in range(0, gridHeight):
        for j in range(0, gridWidth):
            if grid[i][j] == '#':
                if i + 99 < gridHeight and j + 99 < gridWidth:
                    if grid[i][j + 99] == '.':
                        break
                    if grid[i + 99][j] == '#' and grid[i][j + 99] == '#':
                        return (j + offSetX, i + offSetY)


printGrid(grid)
print 'AFFECTED POINTS: ' + str(beamAffected)
shipPos = findShip(grid)
print 'POS Of SHIP: ' + str(shipPos)
print 'ANSEER: ' + str(shipPos[0] * 10000 + shipPos[1])
