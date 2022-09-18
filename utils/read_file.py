import os

class Data:
    def __init__(self, n, w, dimensions):
        self.n = n
        self.w = w
        self.dimensions = dimensions
        
def readFile(i):
    cur_path = os.path.dirname(__file__)
    rel_path = f'../instances/ins-{i}.txt'
    with open(cur_path+'\\'+rel_path, 'r') as f:
        w = [int(x) for x in next(f).split()][0]
        n = [int(x) for x in next(f).split()][0]
        array = []
        for line in f: # read rest of lines
            array.append([int(x) for x in line.split()])
        return Data(n, w, array)