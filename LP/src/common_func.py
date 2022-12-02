from pulp import *
cur_path = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(
    cur_path,
    os.pardir,
    os.pardir)
)
sys.path.append(PROJECT_ROOT)
from utils import Solution, ReadData


def solve(constraints, solver, data: ReadData, rotation: bool = False):
    problem = LpProblem('VLSI', LpMinimize)
    for constraint in constraints:
        problem += constraint
    solver = get_solver(solver)
    timeout = 300
    solver.timeLimit = timeout
    startTime = time()
    problem.solve(solver)
    endTime = time()
    elapsedTime = endTime - startTime
    result = LpStatus[problem.status]
    x = []
    y = []
    l = 0
    r = None
    if rotation:
        r = []
    for var in problem.variables():
        key, val = var.name, round(var.value())
        keyComponents = key.split('_')
        if keyComponents[0] == 'b' and keyComponents[1] == '1':
            print(key, val)
        if keyComponents[0] == 'x':
            x.append(val)
        elif keyComponents[0] == 'y':
            y.append(val)
        elif rotation and keyComponents[0] == 'r':
            r.append(val)
        elif keyComponents[0] == 'l':
            l = val

    if elapsedTime >= timeout:
        return Solution(elapsedTime, [], [], 0, r)
    if result == 'Optimal':
        return Solution(elapsedTime, x, y, l, r)
    return Solution(elapsedTime, x, y, l, r)
