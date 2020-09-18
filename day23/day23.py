import sys
import copy
from sets import Set

file = open(sys.argv[1], 'r')

programInit = file.readline().rstrip("\n\r").split(',')


def runProgram(program, inputSignals, curIns, relativeBase, inputSignalCount):
    i = curIns
    outputs = []
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
            toSet = -1
            if inputSignalCount < len(inputSignals):
                toSet = inputSignals[inputSignalCount]
                inputSignalCount += 1
            program[int(program[i + 1])
                    + (relativeBase if mode1 == 2 else 0)] = toSet
            i += 2
            if toSet == -1:
                return (program, outputs, False, i, relativeBase,
                        inputSignalCount)
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
            if len(outputs) == 3:
                return (program, outputs, False, i, relativeBase,
                        inputSignalCount)
        elif opcode == 9:
            relativeBase += firstParam
            i += 2
        else:
            print 'NOPE'
            exit(1)
    return (program, outputs, halted, i, relativeBase, inputSignalCount)


class Computer:
    def __init__(self, address, program):
        self.address = address
        self.program = program
        self.relativeBase = 0
        self.curIns = 0
        self.inputSignalCount = 0
        self.inputs = [address]
        self.isNat = False

    def setNAT(self):
        self.isNat = True

    def recievePacket(self, packet):
        if self.isNat:
            self.inputs = packet
        else:
            self.inputs += packet

    def hasEmptyQueue(self):
        return self.inputSignalCount == len(self.inputs)

    def runProgram(self):
        (program, outputs, halted,
         i, relativeBase, inputSignalCount) = runProgram(
             self.program, self.inputs, self.curIns, self.relativeBase,
             self.inputSignalCount)
        self.curIns = i
        self.relativeBase = relativeBase
        self.inputSignalCount = inputSignalCount
        self.program = program
        return outputs

    def __str__(self):
        return 'Address: ' + str(self.address) + ', cur q: ' + str(self.inputs)

    __repr__ = __str__


def printComps(computers):
    for comp in computers:
        print comp

program = programInit + ([0] * 4096)

computers = []

for i in range(0, 50):
    computers.append(Computer(i, copy.deepcopy(program)))

nat = []

isIdle = True
lastNatSent = 0
natSent = -1
while lastNatSent != natSent:
    isIdle = True
    for i in range(0, 50):
        isWaiting = computers[i].hasEmptyQueue()
        outputs = computers[i].runProgram()
        # print 'From ' + str(i) + ', out: ' + str(outputs)
        if len(outputs) == 0:
            isIdle = isIdle and isWaiting
        if len(outputs) == 3:
            isIdle = False
            if outputs[0] == 255:
                nat = outputs[1:]
            else:
                computers[outputs[0]].recievePacket(outputs[1:])
        # printComps(computers)
    if isIdle and len(nat) > 0:
        print 'SEND NAT: ' + str(nat)
        lastNatSent = natSent
        computers[0].recievePacket(nat)
        natSent = nat[1]


print 'ANS ' + str(outputs)
printComps(computers)
print 'NAT: ' + str(nat)
