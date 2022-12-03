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


def cumulative(s, d, r, b, name):
    early = 0
    late = max([s[i].upBound + d[i] for i in range(len(s))]) + 1
    constraints = []
    for t in range(early, late):
        sum_vars = 0
        for i in range(len(s)):
            t1 = LpVariable(f't1_{t}_{i}_{name}', 0, 1, LpBinary)
            t2 = LpVariable(f't2_{t}_{i}_{name}', 0, 1, LpBinary)
            t3 = LpVariable(f't3_{t}_{i}_{name}', 0, 1, LpBinary)
            constraints += leq_encoding(s[i], t, t1)
            constraints += geq_encoding(s[i], t + 1 - d[i], t2)
            constraints += and_encoding(t1, t2, t3)
            sum_vars += r[i] * t3
        constraints += [b >= sum_vars]
    return constraints


def leq_encoding(x, t, b):
    constraints = []
    M1 = -t + max(x.upBound, x.lowBound)
    M2 = t + 1 + max(-x.upBound, -x.lowBound)
    constraints += [x <= t + M1 * (1 - b)]  # x + M1*b <= t + M1
    constraints += [-x <= -t - 1 + M2 * b]  # -x -M2*b <= -t-1
    return constraints


def geq_encoding_rot(x, t, d, r, rot, b):
    constraints = []
    M1 = -t + d + max(x.upBound, x.lowBound) + r
    M2 = t + 1 + max(-x.upBound, -x.lowBound)
    # t - d  + d*rot - r*rot
    constraints += [x <= t - ((1 - rot) * d + rot * r) + M1 * b]
    # -t-1 + d -d*rot + r*rot
    constraints += [-x <= -t - 1 + (1 - rot) * d + rot * r + M2 * (1 - b)]
    return constraints


def geq_encoding(x, t, b):
    return leq_encoding(x, t - 1, 1 - b)


def and_encoding(p, q, b):
    constraints = []
    constraints += [2 - (p + q) >= (1 - b)]
    constraints += [b <= p]
    constraints += [b <= q]
    return constraints


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
    obj = [(l, 'minimize l')]
    xBounds = [(blocksX[i] + widths[i] <= w,
                f'xbound_{i}') for i in range(n)]
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
