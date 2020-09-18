import sys
import copy
import math
import time
from functools import reduce
from sets import Set

file = open(sys.argv[1], 'r')
lines = file.readlines()

start = int(round(time.time() * 1000.0))
print "Start Time =" + str(start)

deckSize = 119315717514047
# deckSize = 10007


def modInverse(a, m):
    return pow(a, m - 2, m)


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinvGen(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m(a, m)


def printDeck(deck):
    for i in deck:
        print i


def dealToNewStack(inc, off):
    inc = (inc * -1) % deckSize
    return (inc, (off + inc) % deckSize)


def cutNCards(inc, off, n):
    return (inc, (off + inc * n) % deckSize)


def inv(a, n):
    return pow(a, n - 2, n)


def dealWithIncrementN(inc, off, n):
    return ((inc * inv(n, deckSize)) % deckSize, off)


def printShuffles(shuffles):
    for shfu in shuffles:
        print shfu


position = 2020
shufflesToMake = 101741582076661
# shufflesToMake = 1


shuffles = []
for line in lines:
    shuffles.append(line.rstrip('\r\n'))

offset, increment = 0, 1
for shuffle in shuffles:
    if shuffle == 'deal into new stack':
        (increment, offset) = dealToNewStack(increment, offset)
    elif shuffle[0:3] == 'cut':
        splitIn = shuffle.split(' ')
        (increment, offset) = cutNCards(increment, offset, int(splitIn[-1]))
    elif shuffle[0:4] == 'deal':
        splitIn = shuffle.split(' ')
        (increment, offset) = dealWithIncrementN(increment, offset,
                                                 int(splitIn[-1]))

Ma = pow(increment, shufflesToMake, deckSize)
Mb = (offset * (Ma - 1) * inv(increment - 1, deckSize)) % deckSize

print 'ANSSSS: ' + str(((position - Mb) * inv(Ma, deckSize)) % deckSize)

end = int(round(time.time() * 1000.0))
print 'DONE IN ' + str(end - start)
print 'OTHER: ' + str((Ma * position + Mb) % deckSize)
