from minizinc import Instance, Model, Solver
import os


for i in range(1, 40):
    cur_path = os.path.dirname(__file__)
    print(cur_path)
    new_path = os.path.relpath(f'instances\\ins-{i}.txt', cur_path)
    print(new_path)
    with open(new_path, 'r') as f:
        w = [int(x) for x in next(f).split()]
        h = [int(x) for x in next(f).split()]
        array = []
        for line in f: # read rest of lines
            array.append([int(x) for x in line.split()])


## Load n-Queens model from file
#nqueens = Model("./nqueens.mzn")
## Find the MiniZinc solver configuration for Gecode
#gecode = Solver.lookup("gecode")
## Create an Instance of the n-Queens model for Gecode
#instance = Instance(gecode, nqueens)
## Assign 4 to n
#instance["n"] = 4
#result = instance.solve()
## Output the array q
#print(result["q"])