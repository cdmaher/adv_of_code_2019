import sys
from sets import Set

width = 25
height = 6

file = open(sys.argv[1], 'r')

pixels = list(file.readline().rstrip("\r\n"))

layers = []
i = 0
layerNum = 0
while i < len(pixels):
    layers.append([])
    for y in range(0, height):
        layers[layerNum].append([])
        for x in range(0, width):
            layers[layerNum][y].append(int(pixels[i]))
            i += 1
    layerNum += 1


def renderImage(allLayers):
    finalImage = []
    for i in range(0, height):
        finalImage.append([])
        for j in range(0, width):
            layerNum = 0
            while layerNum < len(layers):
                if (layers[layerNum][i][j] != 2):
                    finalImage[i].append(layers[layerNum][i][j])
                    break
                layerNum += 1
    return finalImage

def printLayer(layerToPrint):
    for i in range(0, height):
        for j in range(0, width):
            if layerToPrint[i][j] == 0:
                print ' ',
            else:
                print '*',
        print ''

print 'Layers: ' + str(layers)
print 'Layer Len: ' + str(len(layers))
print 'Final Image: '
printLayer(renderImage(layers))


def layerZeroCount(layer):
    zeroCount = 0
    for i in range(0, len(layer)):
        for j in range(0, len(layer[i])):
            if layer[i][j] == 0:
                zeroCount += 1
    return zeroCount

def oneByTwoNum(layer):
    oneCount = 0
    twoCount = 0
    for i in range(0, len(layer)):
        for j in range(0, len(layer[i])):
            if layer[i][j] == 1:
                oneCount += 1
            elif layer[i][j] == 2:
                twoCount += 1
    return oneCount * twoCount


# Part 1
# leastZeros = 324234
# leastZeroLayer = 8
# for i in range(0, len(layers)):
#     curZeroCount = layerZeroCount(layers[i])
#     if (curZeroCount < leastZeros):
#         leastZeros = curZeroCount
#         leastZeroLayer = i
#
# print 'Layers: ' + str(layers)
# print 'Least Zeros: ' + str(leastZeros)
# print 'Least Zero Layer: ' + str(leastZeroLayer)
# print 'Least Zero Layer Printed: ' + str(layers[leastZeroLayer])
# print 'Multiply: ' + str(oneByTwoNum(layers[leastZeroLayer]))
