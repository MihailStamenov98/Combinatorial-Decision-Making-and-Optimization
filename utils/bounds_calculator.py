from utils.read_file import ReadData


def chipMaxHeight(data: ReadData, rotation: bool) -> int:
    maxBlockHeight = max(data.dimensions[1]) if not rotation else max(
        max(data.dimensions[1]), max(data.dimensions[0]))
    maxBlockWidth = None
    sumHeights = 0
    if not rotation:
        maxBlockWidth = max(data.dimensions[0])
        sumHeights = sum(data.dimensions[1])
    else:
        maxBlockWidth = data.dimensions[0][0]
        for i in range(data.n):
            sumHeights += min(data.dimensions[1][i], data.dimensions[0][i]
                              if data.dimensions[1][i] <= data.w else data.dimensions[1][i])
            for j in range(2):
                if data.dimensions[j][i] > maxBlockWidth and data.dimensions[j][i] < data.w:
                    maxBlockWidth = data.dimensions[j][i]
    minBlocksOnRow = (data.w // maxBlockWidth)
    chipMaxHeightByArea = maxBlockHeight * (data.n // minBlocksOnRow if data.n % minBlocksOnRow == 0
                                            else (data.n // minBlocksOnRow) + 1)
    return min(chipMaxHeightByArea, sumHeights)
    # return chipMaxHeightByArea


def chipMinHeight(data: ReadData) -> int:
    areaOfBlocks = sum([data.dimensions[0][i] * data.dimensions[1][i]
                       for i in range(data.n)])
    minHeight = max(max(data.dimensions[1]), areaOfBlocks // data.w)
    return minHeight
