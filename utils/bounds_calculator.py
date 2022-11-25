from utils.read_file import ReadData
def chipMaxHeight(data: ReadData, rotation: bool) -> int:
    maxBlockHeight = max(data.dimensions[1]) if not rotation else max(max(data.dimensions[1]), max(data.dimensions[0]))
    maxBlockWidth = max(data.dimensions[0]) if not rotation else maxBlockHeight
    minBlocksOnRow = (data.w // maxBlockWidth)
    chipMaxHeight = maxBlockHeight * ( data.n // minBlocksOnRow if data.n % minBlocksOnRow == 0 
                                            else (data.n // minBlocksOnRow) + 1 )
    return chipMaxHeight

def chipMinHeight(data: ReadData) -> int:
    areaOfBlocks = sum([data.dimensions[0][i] * data.dimensions[1][i] for i in range(data.n)])
    minHeight = max(max(data.dimensions[1]), areaOfBlocks//data.w)
    return minHeight