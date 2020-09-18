import sys
import copy
import math
from functools import reduce
from sets import Set

file = open(sys.argv[1], 'r')
lines = file.readlines()

basePattern = [0, 1, 0, -1]


def xTimesPatternAndShift(pattern, x):
    pattern = reduce(lambda xed, element: xed + [element] * x, pattern, [])
    firstEl = pattern[0]
    pattern = pattern[1:]
    pattern.append(firstEl)
    return pattern


def runPhase(inpList):
    patternX = 1
    ran = 0
    output = []
    while ran < len(inpList):
        newOut = 0
        patternInd = 0
        pattern = xTimesPatternAndShift(copy.deepcopy(basePattern), patternX)
        for i in range(0, len(inpList)):
            newOut += int(inpList[i]) * pattern[patternInd]
            patternInd = (patternInd + 1) % len(pattern)
        patternX += 1
        ran += 1
        inpList[ran] = newOut
    newNum = map(lambda x: str(x)[-1], output)
    asInt = reduce(lambda num, element: num + element, newNum, '')
    return newNum


def runPhase2(inpList):
    ran = 0
    newOut = 0
    for i in range(0, len(inpList)):
        newOut += inpList[i]
    prev = inpList[ran]
    inpList[ran] = newOut % 10
    ran += 1
    while ran < len(inpList):
        newInp = (inpList[ran - 1] - prev + 10) % 10
        prev = inpList[ran]
        inpList[ran] = newInp
        ran += 1
    return inpList


initInput = lines[0].rstrip("\r\n")

phasesToRun = 100
count = 0
curInput = list(str(initInput))
messageOffsetStr = curInput[0:7]
messageOffset = int(
    reduce(lambda num, element: num + element, messageOffsetStr, ''))
print 'Message off ' + str(messageOffset)

curInput = curInput * 10000
curInput = curInput[messageOffset:]
curInput = map(lambda x: int(x), curInput)

print 'len of ' + str(len(curInput))

while count < phasesToRun:
    curInput = runPhase2(curInput)
    print 'phase done ' + str(count)
    count += 1

print 'huh ' + str(curInput) + str(len(curInput))
curInput = reduce(lambda num, element: num + str(element), curInput, '')
print 'Phase ' + str(count) + ', out: ' + str((int(curInput)))
print 'ANSSSSS: ' + str(curInput[0:8])
