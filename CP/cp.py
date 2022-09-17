from minizinc import Instance, Model, Solver
import os

chip_width = "chip_width"
n_blocks = "n_blocks"
dimensions = "dimensions"
chip_height = "chip_height"

for i in range(1, 2):
    cur_path = os.path.dirname(__file__)
    rel_path = f'../instances/ins-{i}.txt'
    with open(cur_path+'\\'+rel_path, 'r') as f:
        w = [int(x) for x in next(f).split()][0]
        n = [int(x) for x in next(f).split()][0]
        array = []
        for line in f: # read rest of lines
            array.append([int(x) for x in line.split()])
        model = Model(cur_path+"\\VLSI.mzn")
        gecode = Solver.lookup("gecode")
        instance = Instance(gecode, model)
        instance[chip_width] = w
        instance[n_blocks] = n
        instance[dimensions] = array
        result = instance.solve()
        #print(result["blocks_x"])
        #print(result["blocks_y"])
        #print(result[chip_width])


