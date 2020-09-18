import sys
from sets import Set

high = 585159
low = 134564


def testAdjacent(number):
    numArr = [int(d) for d in str(number)]
    hasDup = False
    i = 0
    while i < len(numArr) - 1:
        if numArr[i] == numArr[i + 1]:
            if i == len(numArr) - 2:
                return True
            elif numArr[i] != numArr[i + 2]:
                return True
        curr = numArr[i]
        while i < len(numArr) - 1 and numArr[i] == curr:
            i += 1
    return False


def testNotDecreasing(number):
    numArr = [int(d) for d in str(number)]
    for i in range(0, len(numArr) - 1):
        if numArr[i] > numArr[i + 1]:
            return False
    return True


for x in range(low, high + 1):
    if testAdjacent(x) and testNotDecreasing(x):
        print 'FOund: ' + str(x)
