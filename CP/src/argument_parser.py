import argparse
from tkinter import SEL_FIRST
from my_types import ModelType

class ReturnType:
    def __init__(self, args):
        solverStrategyes = []
        if args.gecode:
            solverStrategyes = [(1,3), (2,3), (3,1), (4,1), (4,2), (5,3)]
        else:
            solverStrategyes = [(1,3), (2,2), (2,1), (5,3), (5, 2)]

        filteredSolverStrategyes = []
        if args.search is not None and args.restart is not None:
            filteredSolverStrategyes = [(args.search, args.restart)]
        elif args.restart is not None:
            filteredSolverStrategyes = list(filter(lambda x: (x[1] == args.restart), solverStrategyes))
        elif args.search is not None:
            filteredSolverStrategyes = list(filter(lambda x: (x[0] == args.search), solverStrategyes))

        if args.all:
            self.solverStrategyes = solverStrategyes
        elif filteredSolverStrategyes != []:
            self.solverStrategyes = filteredSolverStrategyes
        else:
            self.solverStrategyes = [(5,2)]
        self.solver = "gecode" if args.gecode else "chuffed"
        self.modelToUse = ModelType.rotated.value if args.rotation else ModelType.normal.value
        self.rotated = args.rotation
        self.draw = args.draw
        self.instances = [args.instance] if args.instance is not None else range(35, 41)


def parsArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--instance", help="Instance on which to run the model, default is all", type=int)
    parser.add_argument("-r", "--rotation", help="Flag to decide whether it is possible use rotated circuits, default is not rotated", action='store_true')
    parser.add_argument("-d", "--draw", help="Flag to decide whether to draw a the solution, default is false", action='store_true')
    parser.add_argument("-g", "--gecode", help="Flag to use Gecoden", action='store_true')
    parser.add_argument("-s", "--search", help = '''Search type (1 input\_order indomain\_min
                                                                2 first\_fail indomain\_min
                                                                3 first\_fail indomain\_random 
                                                                4 dom\_w\_deg indomain\_random
                                                                5 (sorted by area) indomain\_order), 
                                                                default 5''',required=False, type=int)
    parser.add_argument("-res", "--restart", help = '''Restart type (1 restart_linear(100)
                                                                2 restart_luby(100)
                                                                3 restart_none 
                                                                default 3''',required=False, type=int)
    parser.add_argument("-all", "--all", help="Flag to decide whether to run all searches",
                        required=False, action='store_true')
    args = parser.parse_args()
    returnType = ReturnType(args)
    return returnType
