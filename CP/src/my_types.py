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
    normal = "model.mzn"
    rotated = "model_rotation.mzn"
