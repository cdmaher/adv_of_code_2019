import sys
import copy
import math
from functools import reduce
from sets import Set

file = open(sys.argv[1], 'r')
lines = file.readlines()

funcB = 'L,6,R,12,R,8,L,8'
funcA = 'L,6,R,12,L,6,L,8,L,8'
funcC = 'L,4,L,4,L,6'

curLine = lines[0].rstrip("\r\n")

routine = ''
while len(curLine) > 0:
    if curLine[:len(funcA)] == funcA:
        routine += 'A,'
        curLine = curLine[len(funcA):].lstrip(',')
    elif curLine[:len(funcB)] == funcB:
        routine += 'B,'
        curLine = curLine[len(funcB):].lstrip(',')
    elif curLine[:len(funcC)] == funcC:
        routine += 'C,'
        curLine = curLine[len(funcC):].lstrip(',')

routine = routine.rstrip(',')

print 'Routine ' + routine
print 'no ' + curLine

def toAscii(tochrs):
    return map(lambda char: ord(char), list(tochrs)) + [ord('\n')]


intInput = toAscii(routine) + toAscii(funcA) + toAscii(funcB) + toAscii(funcC)
print str(reduce(lambda total, inp: total + str(inp) + ',', intInput, ''))
