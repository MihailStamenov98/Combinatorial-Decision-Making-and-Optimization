from pulp import *
import os
import sys
cur_path = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(
    cur_path,
    os.pardir,
    os.pardir)
)
sys.path.append(PROJECT_ROOT)
from utils import ReadData


def solveInstanceRotated(data: ReadData, minHeight: int, maxHeight: int):
    widths = data.dimensions[0]
    heights = data.dimensions[1]
    n = data.n
    w = data.w
    rotations = [LpVariable(f'r_{i}', lowBound=0,
                            upBound=1, cat=LpBinary) for i in range(n)]
    blocksX = [LpVariable(
        f'x_{i}', lowBound=0, upBound=w - widths[i], cat=LpInteger) for i in range(n)]
    blocksY = [LpVariable(f'y_{n}', lowBound=0, upBound=maxHeight -
                          heights[i], cat=LpInteger) for i in range(n)]
    l = LpVariable('l', lowBound=minHeight, upBound=maxHeight, cat=LpInteger)
    l.setInitialValue(minHeight)
    obj = [(l, 'minimize l')]
    yBounds = [blocksY[i] + heights[i] - l <= 0 for i in range(n)]
    noOverlap = []
    for i in range(n):
        for j in range(i + 1, n):

            b = [LpVariable(f'b_{i}_{j}_{k}', lowBound=0,
                            upBound=1, cat=LpBinary) for k in range(2)]
            noOverlap += [b[0] * (blocksX[i] + widths[i] -
                                  blocksX[j] + b[1] * w <= 0)]
            noOverlap += [b[0] * (blocksX[j] + widths[j] -
                                  blocksX[i] + (1 - b[1]) * w <= 0)]
            noOverlap += [(1 - b[0]) * (blocksY[i] + heights[i] -
                                        blocksY[j] + b[1] * l <= 0)]
            noOverlap += [(1 - b[0]) * (blocksY[j] + heights[j] -
                                        blocksY[i] + (1 - b[1]) * l <= 0)]

    constraints = obj + yBounds + noOverlap

    return constraints
