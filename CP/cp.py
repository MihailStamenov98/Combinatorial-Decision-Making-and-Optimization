from typing import List
import os
from time import time
import sys
import subprocess
from my_types import BlocksDistribution, Constants
from argument_parser import parsArguments
cur_path = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(
    cur_path,
    os.pardir)
)
sys.path.append(PROJECT_ROOT)
from utils import writeFile, WriteData, readFile, Folder, computeMaxHeight

def decodeMinizincOutput(result, i):
    time = 300000
    h = None
    valid = False
    optimal = False

    while result.split(os.linesep)[0].startswith('%') or result.split(os.linesep)[0].startswith('WARNING'):
        if "solveTime" in result.split(os.linesep)[0]:
            time = float(result.split(os.linesep)[0].split("=")[-1])
            print(f"Solution found in time {time:.3f}")
        result = os.linesep.join(result.split(os.linesep)[1:])

    if result.split(os.linesep)[0] == "=====UNKNOWN=====":
        print(f"Could not find a result for instance {i}")

    else:
        try:
            w = int(result.split(os.linesep)[0])
        except ValueError:
            print("Could not parse w as int. Output was:")
            print(result)
            exit(1)
        h = int(result.split(os.linesep)[1])
        n = int(result.split(os.linesep)[2])
        p_x = result.split(os.linesep)[3].replace('[', '').replace(']', '')
        p_x = [int(s) for s in p_x.split(',')]
        p_y = result.split(os.linesep)[4].replace('[', '').replace(']', '')
        p_y = [int(s) for s in p_y.split(',')]
        x = result.split(os.linesep)[5].replace('[', '').replace(']', '')
        x = [int(s) for s in x.split(',')]
        y = result.split(os.linesep)[6].replace('[', '').replace(']', '')
        y = [int(s) for s in y.split(',')]
def solveExample(i, args, strategy):
    data = readFile(i)
    model.output_type = BlocksDistribution
    chipMaxHeight = computeMaxHeight(data.dimensions, data.w)
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
    startTime = time()
    result = instance.solve().solution
    elapsedTime = time() - startTime
    coordinates = list(zip(result.blocks_x, result.blocks_y))
    elapsedTime = f'{elapsedTime * 1000:.1f} ms'
    writeData = WriteData(data.n, data.w, result.h,
                          data.dimensions, coordinates, elapsedTime, result.flipped)
    writeFile(i, Folder.CP.value, writeData)

def main():
    args = parsArguments()    
    for strategy in args.solverStrategy:
        for instance in args.instances:
            command = f'minizinc -s --time-limit {300000} --solver chuffed -f model.mzn "./instances_dzn/ins-{instance}.dzn"'
            result = subprocess.getoutput(command)
            decodeMinizincOutput(result, instance)


if __name__ == '__main__':
    main()
