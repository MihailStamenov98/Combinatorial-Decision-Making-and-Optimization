from my_utils import *
import os
import sys
import time
from z3 import *
from local_types import ResultModel
cur_path = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(
    cur_path,
    os.pardir,
    os.pardir)
)
sys.path.append(PROJECT_ROOT)
from utils import ReadData, Solution
from common_model_finctions import getPossibleSetsOfCirquit


def solveInstance(data: ReadData, encoding: EncodingType, minHeight: int, maxHeight: int) -> ResultModel | Solution:
    # we define a 3 dimensional vector (1d width, 2d height, 3d circuits)
    widths = data.dimensions[0]
    heights = data.dimensions[1]
    blocksX = [[Bool(f"x{block}_{x}") for x in range(data.w)]
               for block in range(data.n)]
    blocksY = [[Bool(f"y{block}_{y}") for y in range(maxHeight)]
               for block in range(data.n)]
    # length of the plate to minimize
    l = [Bool(f"l_{i}") for i in range(minHeight, maxHeight + 1)]
    solver = Solver()

    blockFromBools = []
    for block in range(data.n):
        constructBlockX = getPossibleSetsOfCirquit(
            data.w, widths[block], blocksX[block], encoding, f'exactly_one_blockX_{block}')
        blockFromBools.append(constructBlockX)
        constructBlockY = getPossibleSetsOfCirquit(
            maxHeight, heights[block], blocksY[block], encoding, f'exactly_one_blockY_{block}')
        blockFromBools.append(constructBlockY)
    blockFromBools = And(blockFromBools)

    # overlapping
    noOverlapping = []
    for i in range(maxHeight):
        for j in range(data.w):
            line = [And(blocksX[block][j], blocksY[block][i])
                    for block in range(data.n)]
            noOverlapping.append(
                atMostOne(line, encoding, f'noOverlapping_{i}_{j}'))
    noOverlapping = And(noOverlapping)

    # symmetry breaking
    symmetryBreaking = [lexLessEq(blocksX + blocksY,
                                  [[blocksX[block][i] for i in reversed(range(data.w))] for block in range(data.n)] + blocksY)]

    symmetryBreaking += [lexLessEq(blocksX + blocksY,
                                   blocksX + [[blocksY[block][i] for i in reversed(range(maxHeight))] for block in range(data.n)])]

    symmetryBreaking += [lexLessEq(blocksX + blocksY,
                                   [[blocksX[block][i] for i in reversed(range(data.w))] for block in range(data.n)] +
                                   [[blocksY[block][i] for i in reversed(range(maxHeight))] for block in range(data.n)])]
    symmetryBreaking = And(symmetryBreaking)
    # compute the length consistent wrt the actual circuits positioning
    lengthOfChip = []
    for i in range(minHeight - 1, maxHeight):
        row = [Or([blocksY[block][i] for block in range(data.n)])]
        for j in range(i + 1, maxHeight):
            row.append(Not(Or([blocksY[block][j] for block in range(data.n)])))
        lengthOfChip.append(l[i - minHeight + 1] == And(row))
    lengthOfChip = And(lengthOfChip)

    solver.add(blockFromBools)
    solver.add(noOverlapping)
    solver.add(lengthOfChip)
    solver.add(symmetryBreaking)
    solver.add(exactlyOne(l, encoding, "oneLength"))
    timeout = 300000
    solver.set("timeout", timeout)

    startTime = time.time()
    hasSolution = False
    model = None
    print("before solve")
    while True:
        if solver.check() == sat:
            model = solver.model()
            executionTime = time.time() - startTime
            if executionTime >= 300:
                break
            # print("x")
            # for b in range(data.n):
            #    print([int(is_true(model[blocksX[b][i]]))
            #           for i in range(data.w)])
            # print("y")
            # for b in range(data.n):
            #    print([int(is_true(model[blocksY[b][i]]))
            #           for i in range(maxHeight)])
            # print("l")
            # print([int(is_true(model[l[i]]))
            #      for i in range(0, maxHeight - minHeight + 1)])
            length = 0
            for k in range(0, maxHeight + 1 - minHeight):
                if model.evaluate(l[k]):
                    length = k + minHeight

            # prevent next model from using the same assignment as a previous model
            solver.add(atLeastOne([l[i - minHeight]
                       for i in range(minHeight, length)]))
            hasSolution = True
        else:
            # break when it is impossible to improve anymore the length
            break
    if hasSolution:
        print("sol")
        executionTime = time.time() - startTime
        return decodeOutput(ResultModel(model, executionTime, False, length), data.n, blocksX, blocksY, maxHeight, data.w)

    elif solver.reason_unknown() == "timeout":
        print("timeout")
        return ResultModel(None, 300, None, None)
    else:
        print("unsat")
        return ResultModel(model, None, True, None)
