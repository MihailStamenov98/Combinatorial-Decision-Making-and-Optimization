def computeMaxHeight(dimensions, w):
    sumHeights = sum(dimensions[1])
    maxX = max(dimensions[0])
    maxY = max(dimensions[1])
    numberOfBlocksOnLine = w // maxX
    maxHeight = -(sumHeights // -numberOfBlocksOnLine)
    maxHeight = maxY if maxHeight < maxY else maxHeight
    return maxHeight
