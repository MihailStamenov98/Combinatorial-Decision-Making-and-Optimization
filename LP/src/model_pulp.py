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


def solveInstance(data: ReadData, minHeight: int, maxHeight: int):
    widths = data.dimensions[0]
    heights = data.dimensions[1]
    n = data.n
    w = data.w

    blocksX = [LpVariable(
        f'x_{i}', lowBound=0, upBound=w - widths[i], cat=LpInteger) for i in range(n)]
    blocksY = [LpVariable(f'y_{i}', lowBound=0, upBound=maxHeight -
                          heights[i], cat=LpInteger) for i in range(n)]
    l = LpVariable('l', lowBound=minHeight, upBound=maxHeight, cat=LpInteger)
    l.setInitialValue(minHeight)
    obj = [(l, 'minimize l')]
    yBounds = [(blocksY[i] + heights[i] <= l,
                f'ybound_{i}') for i in range(n)]
    noOverlap = []
    for i in range(n):
        for j in range(i + 1, n):
            b = [LpVariable(f'b_{i}_{j}_{k}', lowBound=0,
                            upBound=1, cat=LpBinary) for k in range(4)]
            noOverlap += [blocksX[i] + widths[i] -
                          blocksX[j] - b[0] * w <= 0]
            noOverlap += [blocksX[j] + widths[j] -
                          blocksX[i] - b[1] * w <= 0]
            noOverlap += [blocksY[i] + heights[i] -
                          blocksY[j] - b[2] * maxHeight <= 0]
            noOverlap += [blocksY[j] + heights[j] -
                          blocksY[i] - b[3] * maxHeight <= 0]
            noOverlap += [b[0] + b[1] + b[2] + b[3] <= 3]
    constraints = obj + yBounds + noOverlap
    return constraints
