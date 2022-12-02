from predicates_encodings import *
from local_types import ResultModel
import os
import sys
from local_types import EncodingType
cur_path = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(
    cur_path,
    os.pardir,
    os.pardir)
)
sys.path.append(PROJECT_ROOT)
from utils import ReadData, Solution


def atLeastOne(bool_vars):
    return at_least_one(bool_vars)


def atMostOne(bool_vars, type: int, name):
    if type == EncodingType.pairwise.value:
        return at_most_one_np(bool_vars)
    elif type == EncodingType.sequential.value:
        return at_most_one_seq(bool_vars, name)
    elif type == EncodingType.bitwise.value:
        return at_most_one_bw(bool_vars, name)
    elif type == EncodingType.heule.value:
        return at_most_one_he(bool_vars, name)


def exactlyOne(bool_vars, type: int, name):
    if type == EncodingType.pairwise.value:
        return exactly_one_np(bool_vars)
    elif type == EncodingType.sequential.value:
        return exactly_one_seq(bool_vars, name)
    elif type == EncodingType.bitwise.value:
        return exactly_one_bw(bool_vars, name)
    elif type == EncodingType.heule.value:
        return exactly_one_he(bool_vars, name)


def flat(myList):
    return [num for sublist in myList for num in sublist]


def decodeOutput(result: ResultModel, n: int, blocksX, blocksY, maxHeight, w, r=None):
    x = []
    y = []
    for block in range(n):
        for i in range(w):
            if is_true(result.model[blocksX[block][i]]):
                x.append(i)
                break
        for i in range(maxHeight):
            if is_true(result.model[blocksY[block][i]]):
                y.append(i)
                break
    if r is None:
        return Solution(result.time, x, y, result.length, None)
    else:
        return Solution(result.time, x, y, result.length, [is_true(result.model[r[block]]) for block in range(n)])


def boolGreaterEq(x, y):
    return Or(x, Not(y))


def lessEq(x, y):
    return And(
        [boolGreaterEq(x[0], y[0])] +
        [
            Implies(
                And([x[j] == y[j] for j in range(i)]),
                boolGreaterEq(x[i], y[i])
            )
            for i in range(1, len(x))
        ]
    )


def lexLessEq(x1, x2):
    return And([lessEq(x1[0], x2[0])] +
               [
                   Implies(
                       And([And([x1[j][k] == x2[j][k] for k in range(len(x1[j]))])
                           for j in range(i)]),
                       lessEq(x1[i], x2[i])
                   )
                   for i in range(1, len(x1))
    ])
