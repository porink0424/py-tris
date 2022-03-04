from lib.classes import *
from lib.helpers.check import isValidPlace

# 受け取ったdirectedMinoをいけるところまで下に落とす。何個分おとせるかを返す
def Drop(directedMino:DirectedMino, topRowIdx:List[int]) -> int:
    occupiedPositions = GetOccupiedPositions(directedMino)

    dropCount = BOARD_HEIGHT 
    for pos0, pos1 in occupiedPositions:
        dropCount = min(dropCount, abs(topRowIdx[pos0] - pos1) - 1)
    
    return dropCount
