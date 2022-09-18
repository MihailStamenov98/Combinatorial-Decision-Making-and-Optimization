from minizinc import Instance, Model, Solver
from typing import List
from dataclasses import InitVar, dataclass
import os
import sys
cur_path = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(
                  cur_path, 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from utils import readFile


@dataclass
class BlocksDistribution:
    def __init__(self, blocks_x, blocks_y, objective):
        self.blocks_x = blocks_x
        self.blocks_x = blocks_y
        self.chipHeight = objective
    __output_item: InitVar[str]


chipWidth = "chip_width"
nBlocks = "n_blocks"
dimensions = "dimensions"
chipHeight = "chip_height"


for i in range(1, 2):
    data = readFile(i)
    model = Model(cur_path+"\\VLSI.mzn")
    model.output_type = BlocksDistribution
    gecode = Solver.lookup("gecode")
    instance = Instance(gecode, model)
    instance[chipWidth] = data.w
    instance[nBlocks] = data.n
    instance[dimensions] = data.dimensions
    result = instance.solve().solution
    assert type(result) == BlocksDistribution
    print(result.blocks_x)