from enum import Enum


class ResultModel:
    def __init__(self, model, time, isUnsatisfiable, length):
        self.model = model
        self.time = time
        self.isUnsatisfiable = isUnsatisfiable
        self.length = length


class EncodingType(Enum):
    pairwise = 1
    sequential = 2
    bitwise = 3
    heule = 4
