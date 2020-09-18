import sys
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
            if len(outputs) == 2:
                return (program, outputs, False, i, relativeBase)
        elif opcode == 9:
            relativeBase += firstParam
            i += 2
        else:
            print 'NOPE' + str(program[i]) + ' ' + str(i)
            exit(1)
    return (program, outputs, halted, i, relativeBase)


def printPanels(panels, curPos, direction):
    for i in range(0, len(panels)):
        for j in range(0, len(panels[i])):
            if i == curPos[0] and j == curPos[1]:
                if direction == 0:
                    print '^',
                elif direction == 1:
                    print '>',
                elif direction == 2:
                    print 'v',
                else:
                    print '<',
            else:
                toPrint = ' ' if panels[i][j] == 0 else '*'
                print toPrint,
        print ''


addedMemory = programInit + ([0] * 2048)

panels = [[0] * 100 for i in range(100)]
curPos = (20, 20)
panels[curPos[0]][curPos[1]] = 1
painted = set()
curColor = 1
direction = 0
relativeBase = 0
halted = False
curIns = 0
program = addedMemory
while not halted:
    (program, outputs, halted, curIns, relativeBase) = runProgram(
        program, [curColor], curIns, relativeBase)
    if halted:
        break
    print 'To paint: ' + str(outputs[0]) + ' ' + str(curPos)
    panels[curPos[0]][curPos[1]] = outputs[0]
    painted.add(curPos)
    direction = (direction + 4 + (-1 if outputs[1] == 0 else 1)) % 4
    if direction == 0:
        curPos = (curPos[0] - 1, curPos[1])
    elif direction == 1:
        curPos = (curPos[0], curPos[1] + 1)
    elif direction == 2:
        curPos = (curPos[0] + 1, curPos[1])
    else:
        curPos = (curPos[0], curPos[1] - 1)
    curColor = panels[curPos[0]][curPos[1]]

print 'PANELS: '
printPanels(panels, curPos, direction)
print 'PAINTED: ' + str(len(painted))
