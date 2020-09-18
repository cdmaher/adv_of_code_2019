import sys
from sets import Set


def calcFuel(mass):
    curFuel = (mass / 3) - 2
    # print 'cur? ' + str(curFuel)
    if (curFuel <= 0):
        return 0
    else:
        return curFuel + calcFuel(curFuel)

print 'test ' + str(calcFuel(14))
print 'test bleh ' + str(calcFuel(100756))

file = open(sys.argv[1], 'r')

lines = file.readlines()

sum = 0
dups = Set()
for line in lines:
    fuel = calcFuel(int(line))
    sum += fuel

print sum
