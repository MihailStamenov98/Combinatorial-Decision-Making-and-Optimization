from pulp import *
from argument_parser import Solver
cur_path = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(
    cur_path,
    os.pardir,
    os.pardir)
)
sys.path.append(PROJECT_ROOT)
from utils import Solution, ReadData


def solve(constraints, solver: Solver, data: ReadData, rotation: bool = False):
    problem = LpProblem('VLSI', LpMinimize)
    for constraint in constraints:
        problem += constraint
    timeout = 300
    startTime = time()
    if solver.value == Solver.gurobipy.value:
        problem.solve(GUROBI_CMD(msg=0, timeLimit=timeout))
    else:
        problem.solve(PULP_CBC_CMD(msg=0, timeLimit=timeout))
    endTime = time()
    elapsedTime = endTime - startTime
    result = LpStatus[problem.status]
    x = [0] * data.n
    y = [0] * data.n
    l = 0
    r = None
    if rotation:
        r = [0] * data.n
    for var in problem.variables():
        key, val = var.name, round(var.value())
        keyComponents = key.split('_')
        # if keyComponents[0] == 'b' and keyComponents[1] == '9' and keyComponents[2] == '10':
        #    print(key, val)
        if keyComponents[0] == 'x':
            x[int(keyComponents[1])] = val
        elif keyComponents[0] == 'y':
            y[int(keyComponents[1])] = val
        elif rotation and keyComponents[0] == 'r':
            r[int(keyComponents[1])] = val
        elif keyComponents[0] == 'l':
            l = val

    if elapsedTime >= timeout:
        return Solution(elapsedTime, [], [], -1, r)
    if result == 'Optimal':
        return Solution(elapsedTime, x, y, l, r)
    return Solution(elapsedTime, [], [], -1, r)
