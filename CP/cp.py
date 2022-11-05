from typing import List
import os
from time import time
import sys
import subprocess
from create_dzns import createDZN
from my_types import BlocksDistribution, Constants, Solution
from argument_parser import parsArguments
cur_path = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(
    cur_path,
    os.pardir)
)
sys.path.append(PROJECT_ROOT)
from utils import writeFile, WriteData, readFile, Folder, computeMaxHeight

def decodeMinizincOutput(result, i) -> Solution:
    time = 300000
    h = None
    arr = result.splitlines()
    while arr[0].startswith('%') or arr[0].startswith('WARNING'):
        if "time=" in arr[0]:
            time = float(arr[0].split("=")[-1])
            print(f"Solution found in time {time:.3f}")
        arr.pop(0)

    if arr[0] == "=====UNKNOWN=====":
        print(f"Could not find a result for instance {i}")

    else:       
        x = arr[0].replace('[', '').replace(']', '')
        x = [int(s) for s in x.split(',')]
        y = arr[1].replace('[', '').replace(']', '')
        y = [int(s) for s in y.split(',')]
        h = int(arr[2])
        rotated = None
        if len(arr) == 4:
            rotated = arr[3].replace('[', '').replace(']', '')
            rotated = [bool(s) for s in rotated.split(',')]
        return Solution(time, x,y,h, rotated)
        

def main():
    args = parsArguments()
    filesData = [None] *  40
    for strategy in args.solverStrategy:
        for instance in args.instances:
            data = None
            if filesData[instance] is None:
               data = readFile(instance)
               filesData[instance] = data
            else: 
              data = filesData[instance]
            createDZN(instance, args.solverStrategy[0].restart, args.solverStrategy[0].chooseVal, data)
            command = f'minizinc -s --time-limit {300000} --solver chuffed -f model.mzn "./instances_dzn/ins-{instance}.dzn"'
            result = subprocess.getoutput(command)
            print(result)
            solution = decodeMinizincOutput(result, instance)
            coordinates = list(zip(solution.x, solution.y))
            elapsedTime = f'{solution.time * 1000:.1f} ms'
            writeData = WriteData(data.n, data.w, solution.h,
                          data.dimensions, coordinates, elapsedTime, solution.rotated)
            writeFile(instance, Folder.CP.value, writeData)

if __name__ == '__main__':
    main()
