import sys
import copy
from sets import Set

file = open(sys.argv[1], 'r')
inputFile = open(sys.argv[2], 'r')

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
        elif opcode == 9:
            relativeBase += firstParam
            i += 2
        else:
            print 'NOPE'
            exit(1)
    return (program, outputs, halted, i, relativeBase)


program = programInit + ([0] * 4096)

input = inputFile.readline().rstrip("\n\r").split(',')
input = map(lambda x: int(x), input)

(program, outputs, halted, i, relativeBase) = runProgram(program, input, 0, 0)

for out in outputs:
    if out > 128:
        break
    print str(unichr(out)),

print 'FINAL: ' + str(outputs[len(outputs) - 1])
