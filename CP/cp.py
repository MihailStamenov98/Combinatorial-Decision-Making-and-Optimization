from typing import List
import os
import sys
from my_types import BlocksDistribution, Constants
from argument_parser import parsArguments
cur_path = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(
    cur_path,
    os.pardir)
)
sys.path.append(PROJECT_ROOT)
from minizinc import Instance, Model, Solver
from utils import writeFile, WriteData, readFile, Folder, computeMaxHeight


def solveExample(i, args, strategy):
    data = readFile(i)
    gecode = Solver.lookup("gecode")
    model=Model(cur_path+args.modelToUse)
    model.output_type = BlocksDistribution
    chipMaxHeight = computeMaxHeight(data.dimensions, data.w)
    instance = Instance(gecode, model)
    #instance["restart"] = strategy.restart
    #instance["changeVal"] = "input_order"
    instance[Constants.chipWidth.value] = data.w
    instance[Constants.nBlocks.value] = data.n
    if args.rotated:
        instance[Constants.dimensions.value] = data.dimensions
    else:
        instance[Constants.widths.value] = data.dimensions[0]
        instance[Constants.heights.value] = data.dimensions[1]
    instance[Constants.chipMaxHeight.value] = chipMaxHeight
    result = instance.solve().solution
    coordinates = list(zip(result.blocks_x, result.blocks_y))

    writeData = WriteData(data.n, data.w, result.h,
                          data.dimensions, coordinates, result.flipped)
    writeFile(i, Folder.CP.value, writeData)

def main():
    args = parsArguments()
    for strategy in args.solverStrategy:
        for instance in args.instances:
            solveExample(instance, args, strategy)


if __name__ == '__main__':
    main()
