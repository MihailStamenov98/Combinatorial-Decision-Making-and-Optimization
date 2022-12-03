import argparse
from tkinter import SEL_FIRST
from pulp import list_solvers
from enum import Enum


class Solver(Enum):
    pulp = "PULP_CBC_CMD"
    gurobipy = "GUROBI_CMD"


class ReturnType:
    def __init__(self, args):
        self.rotated = args.rotation
        self.draw = args.draw
        self.instances = [
            args.instance] if args.instance is not None else range(1, 41)
        self.solvers = [Solver.pulp] if args.pulp else [
            Solver.gurobipy]
        if args.all:
            self.solvers = [Solver.gurobipy, Solver.pulp]


def parsArguments() -> ReturnType:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--instance", help="Instance on which to run the model, default is all", type=int)
    parser.add_argument(
        "-r", "--rotation", help="Flag to decide whether it is possible use rotated circuits, default is not rotated", action='store_true')
    parser.add_argument(
        "-d", "--draw", help="Flag to decide whether to draw a the solution, default is false", action='store_true')
    parser.add_argument(
        "-p", "--pulp", help="Flag to decide whether use pulp solver, default is not guribo", action='store_true')
    parser.add_argument(
        "-all", "--all", help="Flag to decide whether to try all encodings", action='store_true')
    args = parser.parse_args()
    returnType = ReturnType(args)
    return returnType
