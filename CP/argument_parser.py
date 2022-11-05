import argparse
from tkinter import SEL_FIRST
from my_types import ChooseVariableMethods, ChooseValueForVariableMethods, RestartStyles, ModelType


class SolverStrategy:
    def __init__(self, chooseVar, chooseVal, restart):
        self.chooseVar = chooseVar
        self.chooseVal = chooseVal
        self.restart = restart


class ReturnType:
    def __init__(self, args):
        solveStrategies = []
        for var in ChooseVariableMethods:
            for val in ChooseValueForVariableMethods:
                for r in RestartStyles:
                    solveStrategies.append(SolverStrategy(var, val, r))
        if args.restart:
            solveStrategies = [
                strategy for strategy in solveStrategies if strategy.restart == args.restart]
        if args.chooseVar:
            solveStrategies = [
                strategy for strategy in solveStrategies if strategy.chooseVar == args.chooseVar]
        if args.chooseVal:
            solveStrategies = [strategy for strategy in solveStrategies if strategy.chooseVal == args.chooseVal]

        self.solverStrategy = solveStrategies if args.all else [SolverStrategy(
            ChooseVariableMethods.dom_w_deg, ChooseValueForVariableMethods.indomain_random, RestartStyles.luby)]

        self.modelToUse = ModelType.rotated.value if args.rotation else ModelType.normal.value
        self.rotated = args.rotation
        self.graph = args.graph
        self.draw = args.draw
        self.instances = [args.instance] if args.instance is not None else range(24, 25)


def parsArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--instance", help="Instance on which to run the model, default is all", type=int)
    parser.add_argument("-r", "--rotation", help="Flag to decide whether it is possible use rotated circuits, default is not rotated", action='store_true')
    parser.add_argument("-d", "--draw", help="Flag to decide whether to draw a the solution, default is false", action='store_true')
    parser.add_argument("-g", "--graph", help="Flag to decide whether to draw a graph of the times for execution", action='store_true')
    parser.add_argument("-res", "--restart", help="Restart type (1-constant, 2-linear, 3-geometric, 4-luby, 5-none), default 4-luby",
                        required=False, type=int)
    parser.add_argument("-var", "--chooseVar", help="Variable choice (1 - input_order, 2 - first_fail, 3 - occurrence, 4 - dom_w_deg), default is dom_w_deg",
                        required=False, type=int)
    parser.add_argument("-val", "--chooseVal", help="Ways to constrain a variable are: (1 - indomain_min, 2 - indomain_random) ",
                        required=False, type=int)
    parser.add_argument("-all", "--all", help="Flag to decide whether to run all searches",
                        required=False, action='store_true')
    args = parser.parse_args()
    returnType = ReturnType(args)
    return returnType
