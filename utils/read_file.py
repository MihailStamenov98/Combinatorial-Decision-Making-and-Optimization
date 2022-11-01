import os


class ReadData:
    def __init__(self, n, w, dimensions):
        self.n = n
        self.w = w
        self.dimensions = dimensions


def readFile(i) -> ReadData:
    cur_path = os.path.dirname(__file__)
    rel_path = f'../instances/ins-{i}.txt'
    with open(cur_path+'\\'+rel_path, 'r') as f:
        w = [int(x) for x in next(f).split()][0]
        n = [int(x) for x in next(f).split()][0]
        array = [[],[]]
        for line in f:  # read rest of lines
            lineArr = [int(x) for x in line.split()]
            array[0].append(lineArr[0])
            array[1].append(lineArr[1])

        return ReadData(n, w, array)
