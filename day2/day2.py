import sys
from sets import Set


file = open(sys.argv[1], 'r')

programInit = file.readline().split(',')

def runProgram(program):
    for i in range(0, len(program), 4):
        if int(program[i]) == 1:
            program[int(program[i+3])] = int(program[int(program[i+1])]) + int(program[int(program[i+2])])
        elif int(program[i]) == 2:
            program[int(program[i+3])] = int(program[int(program[i+1])]) * int(program[int(program[i+2])])
        elif int(program[i]) == 99:
            break
    return program

for i in range(0, 99):
    for j in range(0, 99):
        programInit[1] = i
        programInit[2] = j
        newProg = runProgram(list(programInit))
        if newProg[0] == 19690720:
            print 'noun ' + str(i)
            print 'verb ' + str(j)
            print 'ans ' + str(100 * i + j)
            break
    if newProg[0] == 19690720:
        break


print(' '.join(map(str, newProg)))
