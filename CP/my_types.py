from dataclasses import InitVar, dataclass
from enum import Enum

@dataclass
class BlocksDistribution:
    def __init__(self, blocks_x, blocks_y, objective,  flat_board, flipped=None):
        self.blocks_x = blocks_x
        self.blocks_y = blocks_y
        self.h = objective
        self.flipped = flipped
        self.flat_board = flat_board
    __output_item: InitVar[str]


class Constants(Enum):
    chipWidth = "chip_width"
    nBlocks = "n_blocks"
    dimensions = "dimensions"
    chipHeight = "chip_height"
    chipMaxHeight = "chip_max_height"
    widths = "widths"
    heights = "heights"


class ModelType(Enum):
    normal = "\\model.mzn"
    rotated = "\\model_rotated.mzn"


class ChooseVariableMethods(Enum):
    input_order = 1
    first_fail = 2
    occurrence = 3
    dom_w_deg = 4


class ChooseValueForVariableMethods(Enum):
    indomain_min = 1
    indomain_random = 2


class RestartStyles(Enum):
    constant = 1
    linear = 2
    geometric = 3
    luby = 4
    none = 5

class Solution:
    def __init__(self, time, x, y, h, rotated=None):
        self.time = time
        self.x = x
        self.y =y
        self.h = h
        self.rotated = rotated