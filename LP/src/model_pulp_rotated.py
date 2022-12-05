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
    r = [LpVariable(f'r_{i}', lowBound=0,
                    upBound=1, cat=LpBinary) for i in range(n)]
    blocksX = [LpVariable(
        f'x_{i}', lowBound=0, upBound=w - min(widths[i], heights[i]), cat=LpInteger) for i in range(n)]
    blocksY = [LpVariable(f'y_{i}', lowBound=0, upBound=maxHeight -
                          min(widths[i], heights[i]), cat=LpInteger) for i in range(n)]
    l = LpVariable('l', lowBound=minHeight, upBound=maxHeight, cat=LpInteger)
    l.setInitialValue(minHeight)
    obj = [(l, 'minimize l')]
    xBounds = [(blocksX[i] + ((1 - r[i]) * widths[i] + r[i] * heights[i]) <= w,
                f'xbound_{i}') for i in range(n)]
    yBounds = [(blocksY[i] + (r[i] * widths[i] + (1 - r[i]) * heights[i]) <= l,
                f'ybound_{i}') for i in range(n)]
    noOverlap = []
    squareNoteRotated = []
    for i in range(n):
        if widths[i] == heights[i]:
            squareNoteRotated += [r[i] == 0]
        for j in range(i + 1, n):
            b = [LpVariable(f'b_{i}_{j}_{k}', lowBound=0,
                            upBound=1, cat=LpBinary) for k in range(4)]
            noOverlap += [blocksX[i] + ((1 - r[i]) * widths[i] + r[i] * heights[i]) -
                          blocksX[j] - b[0] * w <= 0]
            noOverlap += [blocksX[j] + ((1 - r[j]) * widths[j] + r[j] * heights[j]) -
                          blocksX[i] - b[1] * w <= 0]
            noOverlap += [blocksY[i] + (r[i] * widths[i] + (1 - r[i]) * heights[i]) -
                          blocksY[j] - b[2] * maxHeight <= 0]
            noOverlap += [blocksY[j] + (r[j] * widths[j] + (1 - r[j]) * heights[j]) -
                          blocksY[i] - b[3] * maxHeight <= 0]
            noOverlap += [b[0] + b[1] + b[2] + b[3] <= 3]

    constraints = obj + yBounds + noOverlap + xBounds

    return constraints
