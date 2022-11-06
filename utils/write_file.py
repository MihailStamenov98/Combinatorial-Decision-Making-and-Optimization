from enum import Enum
import os

class WriteData:
    def __init__(self, n, w, h, dimensions, coordinates, time, rotations = None):
        self.n = n
        self.w = w
        self.h = h
        self.dimensions = dimensions
        self.coordinates = coordinates
        self.rotations = rotations
        self.time = time
        
class Folder(Enum):
    CP = "CP"
    SAT = "SAT"
    MIP = "MIP"

def writeFile(i, folder: Folder, data: WriteData) -> str:
    cur_path = os.path.dirname(__file__)
    solutionFolder = 'solution-rotation' if data.rotations is not None else 'solution'
    fileName = f'solution-{i}' if data.rotations is None else f'solution-{i}-with-rotation'
    rel_path = f'../{folder}/{solutionFolder}/{fileName}.txt'
    with open(cur_path+'\\'+rel_path, 'w') as f:
        f.write(f'{data.w} {data.h}\n')
        f.write(f'{data.n}\n')
        n=data.n
        for j in range(n):
            dimensions = f'{data.dimensions[0][j]} {data.dimensions[1][j]}'
            coordinates = f'{data.coordinates[j][0]} {data.coordinates[j][1]}'
            if data.rotations is None:
                f.write(dimensions + " " + coordinates + '\n')
            else:
                f.write(f'{dimensions} {coordinates} {data.rotations[j]}\n')

        f.write(data.time)
    return f'{fileName}'
