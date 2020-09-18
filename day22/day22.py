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

deckSize = 10007


def printDeck(deck):
    for i in deck:
        print i

stupid = 101741582076661 / 100
thing = 0
for j in range(0, 100):
    for i in range(0, stupid):
        thing = 1

def dealToNewStack(deck):
    newDeck = [0] * deckSize
    for i in range(0, len(deck)):
        newDeck[-i - 1] = deck[i]
    return newDeck


def cutNCards(deck, n):
    toCut = deck[0:n]
    deck = deck[n:]
    deck += toCut
    return deck


def dealWithIncrementN(deck, n):
    newDeck = [0] * deckSize
    count = 0
    inc = 0
    while count < deckSize:
        newDeck[inc] = deck[count]
        inc = (inc + n) % deckSize
        count += 1
    return newDeck


deck = []
for i in range(0, deckSize):
    deck.append(i)

shuffles = []
for line in lines:
    shuffles.append(line.rstrip('\r\n'))

for shuffle in shuffles:
    if shuffle == 'deal into new stack':
        deck = dealToNewStack(deck)
    elif shuffle[0:3] == 'cut':
        splitIn = shuffle.split(' ')
        deck = cutNCards(deck, int(splitIn[-1]))
    elif shuffle[0:4] == 'deal':
        splitIn = shuffle.split(' ')
        deck = dealWithIncrementN(deck, int(splitIn[-1]))

printDeck(deck)
print ''
end = int(round(time.time() * 1000.0))
print 'DONE IN ' + str(end - start)
print 'ANS ' + str(deck[2020])
