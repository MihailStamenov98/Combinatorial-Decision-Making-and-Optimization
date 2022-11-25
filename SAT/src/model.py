from my_utils import atLeastOne, atMostOne, exactlyOne, EncodingType, flat
import os
import sys
import time
from z3 import *
cur_path = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(
    cur_path,
    os.pardir,
    os.pardir)
)
sys.path.append(PROJECT_ROOT)
from utils import ReadData, Solution


class ResultModel:
    def __init__(self, model, time, isUnsatisfiable, length):
        self.model = model
        self.time = time
        self.isUnsatisfiable = isUnsatisfiable
        self.length = length


def findFirstTrue(result: ResultModel, cube, cirquit: int, maxHeight, w):
    for i in range(maxHeight):
        for j in range(w):
            if is_true(result.model[cube[i][j][cirquit]]):
                return (j, i)


def decodeOutput(result: ResultModel, n: int, cube, maxHeight, w):
    x = []
    y = []
    length = None
    for i in range(n):
        cirquitX, cirquitY = findFirstTrue(result, cube, i, maxHeight, w)
        x.append(cirquitX)
        y.append(cirquitY)
    return Solution(result.time, x, y, result.length, None)


def solveInstance(data: ReadData, encoding: EncodingType, minHeight: int, maxHeight: int) -> ResultModel | Solution:
    # we define a 3 dimensional vector (1d width, 2d height, 3d circuits)
    cube = [[[Bool(f"cube_{i}_{j}_{k}") for k in range(data.n)]
             for j in range(data.w)] for i in range(maxHeight)]

    # length of the plate to minimize
    l = [Bool(f"l_{i}") for i in range(minHeight - 1, maxHeight)]

    solver = Solver()

    # overlapping
    noOverlapping = []
    for i in range(maxHeight):
        for j in range(data.w):
            noOverlapping += atMostOne(cube[i][j], encoding)

    # create rectangles from bool vars
    allBlocksPositions = []
    # stack up the blocks
    stackUp = [atLeastOne(flat([
        [cube[0][x][block] for x in range(data.w)]
        for block in range(data.n)
    ]))]
    for block in range(data.n):
        blockWidth = data.dimensions[0][block]
        blockHeight = data.dimensions[1][block]
        blockPositions = []
        for i in range(maxHeight - blockHeight + 1):
            for j in range(data.w - blockWidth + 1):
                blockPositionForCoordinates = []
                if i > 0:

                    listOfVarsUnderTheBlock = []
                    bottom = max(0, j - blockWidth + 1)
                    for y in range(bottom, j + blockWidth):
                        for other in range(data.n):
                            listOfVarsUnderTheBlock.append(
                                cube[i - 1][y][other])
                    stackUp.append(
                        Implies(cube[i][j][block],
                                atLeastOne(flat(cube[i - 1]))
                                )
                    )

                for y in range(maxHeight):
                    for x in range(data.w):
                        if i <= y < i + blockHeight and j <= x < j + blockWidth:
                            blockPositionForCoordinates.append(
                                cube[y][x][block])
                        else:
                            blockPositionForCoordinates.append(
                                Not(cube[y][x][block]))
                blockPositions.append(And(blockPositionForCoordinates))
        allBlocksPositions.append(exactlyOne(blockPositions, encoding))
    # compute the length consistent wrt the actual circuits positioning
    lengthOfChip = []
    for i in range(minHeight - 1, maxHeight):
        row = [Or(flat(cube[i]))]
        for j in range(i + 1, maxHeight):
            row.append(Not(Or(flat(cube[j]))))
        lengthOfChip.append(l[i - minHeight] == And(row))
    lengthOfChip = And(lengthOfChip)
    solver.add(noOverlapping)
    solver.add(allBlocksPositions)
    solver.add(stackUp)
    solver.add(lengthOfChip)
    timeout = 300000
    solver.set("timeout", timeout)

    startTime = time.time()
    hasSolution = False
    model = None
    while True:
        if solver.check() == sat:
            model = solver.model()
            length = -1
            for k in range(minHeight, maxHeight):
                if model.evaluate(l[k - minHeight]):
                    length = k

            # prevent next model from using the same assignment as a previous model
            solver.add(atLeastOne([l[i - minHeight]
                       for i in range(minHeight, length)]))
            hasSolution = True
        else:
            # break when it is impossible to improve anymore the length
            break
    if hasSolution:
        length += 1
        executionTime = time.time() - startTime
        return decodeOutput(ResultModel(model, executionTime, False, length), data.n, cube, maxHeight, data.w)

    elif solver.reason_unknown() == "timeout":
        return ResultModel(None, 300, None, None)
    else:
        return ResultModel(model, None, True, None)
