import argparse
from tkinter import SEL_FIRST


class ReturnType:
    def __init__(self, args):
        self.rotated = args.rotation
        self.draw = args.draw
        self.instances = [
            args.instance] if args.instance is not None else range(15, 20)
        self.encodings = [args.encoding] if args.encoding is not None else [1]
        if args.all:
            self.encodings = range(1, 5)


def parsArguments() -> ReturnType:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--instance", help="Instance on which to run the model, default is all", type=int)
    parser.add_argument(
        "-r", "--rotation", help="Flag to decide whether it is possible use rotated circuits, default is not rotated", action='store_true')
    parser.add_argument(
        "-d", "--draw", help="Flag to decide whether to draw a the solution, default is false", action='store_true')
    parser.add_argument(
        "-e", "--encoding", help="The encoding of constraints (1-pairwise, 2-sequential, 3-bitwise, 4-heule)", type=int)
    parser.add_argument(
        "-all", "--all", help="Flag to decide whether to try all encodings", action='store_true')
    args = parser.parse_args()
    returnType = ReturnType(args)
    return returnType
