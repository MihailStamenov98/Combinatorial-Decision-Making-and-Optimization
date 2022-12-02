from z3 import *


def getPossibleSetsOfCirquit(chipSize: int, blockSize: int, varsToUse):
    constructBlock = []
    for x in range(chipSize - blockSize + 1):
        line = []
        for i in range(chipSize):
            if (i >= x and i < x + blockSize):
                line.append(varsToUse[i])
            else:
                line.append(Not(varsToUse[i]))
        constructBlock.append(And(line))
    return constructBlock
