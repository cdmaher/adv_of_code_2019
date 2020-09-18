import sys
from sets import Set

file = open(sys.argv[1], 'r')

programInit = file.readline().rstrip("\n\r").split(',')


def runProgram(program, inputSignals, phaseSetting, usePhaseSetting, curIns):
    i = curIns
    outputs = []
    phaseSettingSet = not usePhaseSetting
    inputSignalCount = 0
    halted = False
    while i < len(program):
        # print 'CUR instr: ' + str(i)
        # print 'CUR prog: ' + str(program)

        opcode = int(program[i]) % 100
        # print 'CUR opcoe: ' + str(opcode)

        if opcode == 99:
            # print 'HALTED!!!!'
            halted = True
            break
        mode1 = (int(program[i]) % 1000) / 100
        mode2 = (int(program[i]) % 10000) / 1000
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
            toSet = phaseSetting
            if phaseSettingSet:
                toSet = inputSignals[inputSignalCount]
                inputSignalCount += 1
            program[int(program[i + 1])] = toSet
            phaseSettingSet = True
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
            outputs.append(firstParam)
            i += 2
            return (program, outputs, False, i)
        else:
            print 'NOPE'
            exit(1)
    return (program, outputs, halted, i)


def runAmplifiers(program, phaseSettings):
    outs = []
    halted = False
    inputSignals = [0]
    count = 0
    curIns = [0, 0, 0, 0, 0]
    lastOut = 0
    programs = [
        list(program),
        list(program),
        list(program),
        list(program),
        list(program)
    ]
    while not halted:
        for i in range(0, len(phaseSettings)):
            (newProg, outs, halted, ins) = runProgram(
                programs[i],
                inputSignals,
                phaseSettings[i],
                count == 0,
                curIns[i],
            )
            if not halted:
                lastOut = outs
            inputSignals = outs
            curIns[i] = ins
            programs[i] = newProg
            # print 'OUTPUTS: ' + str(outs) + ' ' + str(halted)

        # print 'new prog: ' + str(program)

        # print 'hey halted :( ' + str(halted) + ' ' + str(i)
        count += 1
    return lastOut


possiblePhaseSettings = []
for a in range(5, 10):
    for b in range(5, 10):
        for c in range(5, 10):
            for d in range(5, 10):
                for e in range(5, 10):
                    settings = {a, b, c, d, e}
                    if len(settings) == 5:
                        possiblePhaseSettings.append([a, b, c, d, e])
maxVal = 0
bestPhaseSetting = []

for i in range(0, len(possiblePhaseSettings)):
    thruster = runAmplifiers(list(programInit), possiblePhaseSettings[i])
    if thruster[0] > maxVal:
        maxVal = thruster[0]
        bestPhaseSetting = possiblePhaseSettings[i]

print 'Best Setting: ' + str(bestPhaseSetting)
print 'Max Thruster: ' + str(maxVal)
