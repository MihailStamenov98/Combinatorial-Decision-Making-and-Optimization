from typing import List
import os
from time import time
import sys
import subprocess
from create_dzns import createDZN
from my_types import Solution
from argument_parser import parsArguments
cur_path = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(
    cur_path,
    os.pardir,
    os.pardir)
)
sys.path.append(PROJECT_ROOT)
from utils import writeFile, WriteData, readFile, Folder, plotSolution, graph

def decodeMinizincOutput(result, i, rotated: bool) -> Solution:
    time = 300
    h = None
    arr = result.splitlines()
    while arr[0].startswith('%') or arr[0].startswith('Warning') or arr[0].startswith('WARNING:'):
        arr.pop(0)

    if arr[0] == "=====UNKNOWN=====":
        print(f"Could not find a result for instance {i}")
        return None
    if arr[0] == "=====UNSATISFIABLE=====":
        print(f"There is no solution for instance {i}")
        return None

    else:
        x = arr[0].replace('[', '').replace(']', '')
        x = [int(s) for s in x.split(',')]
        arr.pop(0)
        y = arr[0].replace('[', '').replace(']', '')
        y = [int(s) for s in y.split(',')]
        arr.pop(0)
        h = int(arr[0])
        arr.pop(0)
        rotations = None
        if rotated:
            rotations = arr[0].replace('[', '').replace(']', '')
            rotations = ['true' in s for s in rotations.split(',')]
            arr.pop(0)
        if '% time elapsed:' in arr[0]:
            time = float(arr[0].split(":")[1].split(" ")[1])
            print(f"Solution found for instance {i} in time {time:.3f}")  
            arr.pop(0)
        return Solution(time, x,y,h, rotations)
        
def saveTimes(times):
    with open('times.txt', 'w') as f:
        model = 1
        for time in times:
            f.write(f'model number {model}\n')
            model += 1
            isinstance = 1
            for x in time:
                f.write(f'instance-{isinstance} - {x}\n')
                isinstance += 1

def main():
    args = parsArguments()
    filesData = [None] *  40
    times = []
    for strategy in args.solverStrategyes:
        times.append([])
        print(strategy)
        for instance in args.instances:
            data = None
            if filesData[instance-1] is None:
               data = readFile(instance)
               filesData[instance-1] = data
            else: 
              data = filesData[instance-1]
            createDZN(instance, strategy[0], strategy[1], data)
            command = f'minizinc -s --output-time --time-limit {300000} --solver {args.solver} -f {args.modelToUse} "../instances_dzn/ins-{instance}.dzn"'
            result = subprocess.getoutput(command)
            solution = decodeMinizincOutput(result, instance, args.rotated)
            if solution is None:
                times[-1].append("no solution")
                continue
            coordinates = list(zip(solution.x, solution.y))
            elapsedTime = f'{solution.time * 1000:.1f} ms'
            writeData = WriteData(data.n, data.w, solution.h,
                          data.dimensions, coordinates, elapsedTime, solution.rotated)
            fileName = writeFile(instance, Folder.CP.value, writeData)
            times[-1].append(elapsedTime)
            if args.draw:
                fileNmae = ("../solution-rotation/" if args.rotated else "../solution/" ) + fileName + ".png"
                plotSolution(data.w, solution.h, data.n, solution.x, solution.y, data.dimensions[0], data.dimensions[1], elapsedTime, fileNmae, solution.rotated)
    saveTimes(times)    
if __name__ == '__main__':
    main()