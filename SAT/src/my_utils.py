from itertools import combinations
from z3 import *
import math
from enum import Enum


class EncodingType(Enum):
    pairwise = 1
    sequential = 2
    bitwise = 3
    heule = 4

#pairwise
def at_most_one_np(bool_vars, name = ""):
    return [Not(And(pair[0], pair[1])) for pair in combinations(bool_vars, 2)]

def exactly_one_np(bool_vars, name = ""):
    return And(at_least_one(bool_vars), And(at_most_one_np(bool_vars, name)))

#sequential
def at_most_one_seq(bool_vars, name):
    constraints = []
    n = len(bool_vars)
    s = [Bool(f"s_{name}_{i}") for i in range(n - 1)]
    constraints.append(Or(Not(bool_vars[0]), s[0]))
    constraints.append(Or(Not(bool_vars[n-1]), Not(s[n-2])))
    for i in range(1, n - 1):
        constraints.append(Or(Not(bool_vars[i]), s[i]))
        constraints.append(Or(Not(bool_vars[i]), Not(s[i-1])))
        constraints.append(Or(Not(s[i-1]), s[i]))
    return And(constraints)

def exactly_one_seq(bool_vars, name):
    return And(at_least_one(bool_vars), at_most_one_seq(bool_vars, name))


#bitwise
def toBinary(num, length = None):
    num_bin = bin(num).split("b")[-1]
    if length:
        return "0"*(length - len(num_bin)) + num_bin
    return num_bin

def at_most_one_bw(bool_vars, name):
    constraints = []
    n = len(bool_vars)
    m = math.ceil(math.log2(n))
    r = [Bool(f"r_{name}_{i}") for i in range(m)]
    binaries = [toBinary(i, m) for i in range(n)]
    for i in range(n):
        for j in range(m):
            phi = Not(r[j])
            if binaries[i][j] == "1":
                phi = r[j]
            constraints.append(Or(Not(bool_vars[i]), phi))        
    return And(constraints)

def exactly_one_bw(bool_vars, name):
    return And(at_least_one(bool_vars), at_most_one_bw(bool_vars, name))


#heule
def at_most_one_he(bool_vars, name):
    if len(bool_vars) <= 4:
        return And(at_most_one_np(bool_vars))
    y = Bool(f"y_{name}")
    return And(And(at_most_one_np(bool_vars[:3] + [y])), And(at_most_one_he(bool_vars[3:] + [Not(y)], name+"_")))

def exactly_one_he(bool_vars, name):
    return And(at_most_one_he(bool_vars, name), at_least_one(bool_vars))


def at_least_one(bool_vars):
    return Or(bool_vars)

def atLeastOne(bool_vars):
    return at_least_one(bool_vars)

def atMostOne(bool_vars, type: int):
    if type == EncodingType.pairwise.value:
        return at_most_one_np(bool_vars)
    elif type == EncodingType.sequential.value: 
        return at_most_one_seq(bool_vars)
    elif type == EncodingType.bitwise.value: 
        return at_most_one_bw(bool_vars)
    elif type == EncodingType.heule.value: 
        return at_most_one_he(bool_vars)

def exactlyOne(bool_vars, type: int):
    if type == EncodingType.pairwise.value:
        return exactly_one_np(bool_vars)
    elif type == EncodingType.sequential.value: 
        return exactly_one_seq(bool_vars)
    elif type == EncodingType.bitwise.value: 
        return exactly_one_bw(bool_vars)
    elif type == EncodingType.heule.value: 
        return exactly_one_he(bool_vars)

def flat(my_list):
    return [num for sublist in my_list for num in sublist]
