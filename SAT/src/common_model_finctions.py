from z3 import *
from my_utils import exactlyOne
from local_types import EncodingType


def getPossibleSetsOfCirquit(chipSize: int, blockSize: int, varsToUse, encoding: EncodingType, name: str):
    constructBlock = []
    for x in range(chipSize - blockSize + 1):
        line = []
        for i in range(chipSize):
            if (i >= x and i < x + blockSize):
                line.append(varsToUse[i])
            else:
                line.append(Not(varsToUse[i]))
        constructBlock.append(And(line))
    return Or(constructBlock)
