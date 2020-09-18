import sys
import random
import copy
from sets import Set

file = open(sys.argv[1], 'r')

programInit = file.readline().rstrip("\n\r").split(',')


def runProgram(program, inputSignals, curIns, relativeBase, gameInited):
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
            if len(outputs) > 2 and (outputs[-3] == -1 or gameInited):
                return (program, outputs, False, i, relativeBase)
        elif opcode == 9:
            relativeBase += firstParam
            i += 2
        else:
            print 'NOPE' + str(program[i]) + ' ' + str(i)
            exit(1)
    return (program, outputs, halted, i, relativeBase)


def printGameGrid(grid):
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if grid[i][j] == 0:
                print ' ',
            elif grid[i][j] == 3:
                print '_',
            elif grid[i][j] == 4:
                print 'O',
            else:
                print grid[i][j],
        print ''


addedMemory = programInit + ([0] * 2048)


def countBlocks(grid):
    blocks = 0
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if grid[i][j] == 2:
                blocks += 1
    return blocks

def createInputs(xBall, xPaddle, init):
    if init:
        return [1] + [0] * 10
    magnitude = xBall - xPaddle
    dir = -1 if magnitude < 0 else 0 if magnitude == 0 else 1
    if init:
        dir = dir * -1
    inputs = ([dir] * abs(magnitude)) + [0] * 10
    return inputs

def runGameV2():
    segmentDisplay = 0
    gameGrid = [[0] * 50 for i in range(50)]
    newProgram = copy.deepcopy(addedMemory)
    curIns = 0
    curXBall = 0
    curXPaddle = 0
    relativeBase = 0
    gameLost = False
    halted = False
    init = True
    count = 0
    while not halted or gameLost:
        (newProgram, outputs, halted, curIns, relativeBase) = runProgram(
            newProgram,
            createInputs(curXBall, curXPaddle, init),
            curIns,
            relativeBase,
            count > 0
        )
        for i in range(0, len(outputs), 3):
            if outputs[i] == -1 and outputs[i + 1] == 0:
                segmentDisplay = outputs[i + 2]
                if segmentDisplay > 0:
                    print 'NEW SCORE: ' + str(segmentDisplay)
                    print 'BLOCKS: ' + str(countBlocks(gameGrid))
                    printGameGrid(gameGrid)
            else:
                gameGrid[outputs[i + 1]][outputs[i]] = outputs[i + 2]
                if outputs[i + 2] == 4:
                    curXBall = outputs[i]
                elif outputs[i + 2] == 3:
                    curXPaddle = outputs[i]
        count += 1
        if count > 1:
            init = False
        if halted and segmentDisplay == 0:
            gameLost = True
        if count < 30:
            printGameGrid(gameGrid)
    print 'Final: ' + str(segmentDisplay)
    return segmentDisplay

hasWon = False
final = runGameV2()
hasWon = final > 0

print 'FINAL SCORE ' + str(final)
