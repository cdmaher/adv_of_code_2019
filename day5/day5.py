import sys
from sets import Set

file = open(sys.argv[1], 'r')

programInit = file.readline().rstrip("\n\r").split(',')

inputVal = 5


def runProgram(program):
    i = 0
    outputs = []
    while i < len(program):
        opcode = int(program[i]) % 100
        # print 'curprog ' + str(program)
        # print 'cur ' + str(program)
        if opcode == 99:
            break
        mode1 = (int(program[i]) % 1000) / 100
        mode2 = (int(program[i]) % 10000) / 1000
        # print 'op ' + str(opcode)
        # print 'mode 1: ' + str(mode1)
        # print 'mode 2: ' + str(mode2)
        firstParam = int(program[int(program[i + 1])]) if mode1 == 0 else int(
            program[i + 1])
        secondParam = 0
        if opcode == 1 or opcode == 2 or opcode >= 5:
            secondParam = int(program[int(
                program[i + 2])]) if mode2 == 0 else int(program[i + 2])

        if opcode == 1:
            program[int(program[i + 3])] = firstParam + secondParam
            i += 4
        elif opcode == 2:
            program[int(program[i + 3])] = firstParam * secondParam
            i += 4
        elif opcode == 3:
            program[int(program[i + 1])] = inputVal
            i += 2
        elif opcode == 5:
            if firstParam != 0:
                # program[i] = secondParam
                i = secondParam
            else:
                i += 3
        elif opcode == 6:
            if firstParam == 0:
                # program[i] = secondParam
                i = secondParam
            else:
                i += 3
        elif opcode == 7:
            if firstParam < secondParam:
                program[int(program[i + 3])] = 1
            else:
                program[int(program[i + 3])] = 0
            i += 4
        elif opcode == 8:
            if firstParam == secondParam:
                program[int(program[i + 3])] = 1
            else:
                program[int(program[i + 3])] = 0
            i += 4
        elif opcode == 4:
            print 'prev ' + str(program[i - 4]) + ' ' + str(
                program[i - 3]) + ' ' + str(program[i - 2]) + ' ' + str(
                    program[i - 1])
            print 'POS: ' + str(i)
            print 'mode: ' + str(mode1)
            print 'post ' + str(program[i + 1])
            print 'firstparam: ' + str(firstParam)
            outputs.append(firstParam)
            i += 2
    return outputs


outs = runProgram(programInit)
print 'OUT: ' + str(outs)
