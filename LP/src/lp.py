import os
import sys
from common_func import solve
from argument_parser import parsArguments
from model_pulp import solveInstance
from model_pulp_rotated import solveInstanceRotated
cur_path = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(
    cur_path,
    os.pardir,
    os.pardir)
)
sys.path.append(PROJECT_ROOT)
from utils import Solution, writeFile, WriteData, readFile, Folder, plotSolution, chipMinHeight, chipMaxHeight


def saveTimes(times):
    with open('times.txt', 'w') as f:
        model = 1
        for time in times:
            f.write(f'model number {model}\n')
            model += 1
            isinstance = 1
            for x in time:
                f.write(f'{x}\n')
                isinstance += 1


def main():
    args = parsArguments()
    times = []
    for solver in args.solvers:
        times.append([])
        times[-1].append(f'encoding = {solver.value}')
        print(f'encoding = {solver.value}')
        for instance in args.instances:
            data = readFile(instance)
            constraints = None
            maxHeight = chipMaxHeight(data, args.rotated)
            minHeight = chipMinHeight(data)
            if args.rotated:
                constraints = solveInstanceRotated(
                    data, minHeight, maxHeight)
            else:
                constraints = solveInstance(data, minHeight, maxHeight)

            solution = solve(constraints, solver,
                             data, args.rotated == True)
            # print(data.dimensions[0])
            # print(data.dimensions[1])
            # print(solution.x)
            # print(solution.y)
            # print(solution.rotated)
            if solution.x != []:
                coordinates = list(zip(solution.x, solution.y))
                elapsedTime = f'{solution.time * 1000:.1f} ms'
                writeData = WriteData(data.n, data.w, solution.h,
                                      data.dimensions, coordinates, elapsedTime, solution.rotated)
                fileName = writeFile(instance, Folder.LP.value, writeData)
                print(f'inst-{instance} -        {elapsedTime}')
                times[-1].append(elapsedTime)
                if args.draw:
                    fileNmae = (
                        "../out/solution-rotation/" if args.rotated else "../out/solution/") + fileName + ".png"
                    plotSolution(data.w, solution.h, data.n, solution.x, solution.y,
                                 data.dimensions[0], data.dimensions[1], elapsedTime, fileNmae, solution.rotated)
            else:
                print(
                    f'inst-{instance} -        {solution.time * 1000:.1f} ms')

                times[-1].append("not solved")
        times[-1].append('\n')

    saveTimes(times)


if __name__ == '__main__':
    main()
