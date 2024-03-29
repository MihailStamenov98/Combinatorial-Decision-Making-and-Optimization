from my_utils import EncodingType
import os
import sys
from z3 import *
from model import ResultModel
from argument_parser import parsArguments
from model import solveInstance
from model_rotated import solveInstanceRotated
cur_path = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(
    cur_path,
    os.pardir,
    os.pardir)
)
sys.path.append(PROJECT_ROOT)

from utils import Solution, writeFile, WriteData, readFile, Folder, plotSolution, chipMinHeight, chipMaxHeight


def saveTimes(times, instance, encoding):
    with open('times.txt', 'a') as f:
        f.write(f'ins-{instance} enc-{encoding}-            ')
        for time in times:
            for x in time:
                f.write(f'{x}          ')
        # if encoding == 4:
        f.write('\n')


def main():
    args = parsArguments()
    times = []
    for encoding in args.encodings:
        times.append([])
        print(f'encoding = {encoding}')
        for instance in args.instances:
            data = readFile(instance)
            result = None
            maxHeight = chipMaxHeight(data, args.rotated)
            minHeight = chipMinHeight(data)
            if args.rotated:
                result = solveInstanceRotated(
                    data, encoding, minHeight, maxHeight)
            else:
                result = solveInstance(data, encoding, minHeight, maxHeight)
            if type(result) == Solution:
                coordinates = list(zip(result.x, result.y))
                elapsedTime = f'{result.time * 1000:.1f} ms'
                writeData = WriteData(data.n, data.w, result.h,
                                      data.dimensions, coordinates, elapsedTime, result.rotated)
                fileName = writeFile(instance, Folder.SAT.value, writeData)
                times[-1].append(f'{result.time * 1000:.1f}')
                print(f'ins-{instance} -    {elapsedTime}')
                if args.draw:
                    fileNmae = (
                        "../out/solution-rotation/" if args.rotated else "../out/solution/") + fileName + ".png"
                    plotSolution(data.w, result.h, data.n, result.x, result.y,
                                 data.dimensions[0], data.dimensions[1], elapsedTime, fileNmae, result.rotated)
            elif result.model is None and result.isUnsatisfiable:
                times[-1].append("unsatisfiable")
                continue
            elif result.model is None and not result.isUnsatisfiable:
                times[-1].append("no result")
                continue

    saveTimes(times, args.instances[0], encoding)


if __name__ == '__main__':
    main()
