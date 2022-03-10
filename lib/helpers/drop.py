from lib.classes import *
from lib.helpers.check import isValidPlace

# 受け取ったdirectedMinoをいけるところまで下に落とす。何個分おとせるかを返す
# 高速化のため、ミノが今積まれている盤面より上にあるという制約をつける。
def DropFromTop(directedMino:DirectedMino, topRowIdx:List[int]) -> int:
    occupiedPositions = GetOccupiedPositions(directedMino)

    dropCount = BOARD_HEIGHT 
    for pos0, pos1 in occupiedPositions:
        assert topRowIdx[pos0] > pos1
        dropCount = min(dropCount, abs(topRowIdx[pos0] - pos1) - 1)
    
    return dropCount

# 受け取ったdirectedMinoをいけるところまで下に落とす。何個分おとせるかを返す
# こちらの関数は上の関数とは異なり、制約をつけない。
def Drop(mainBoard:List[int], directedMino:DirectedMino) -> int:
    dropCount = 0
    occupiedPositions = GetOccupiedPositions(directedMino)
    occupiedPositions = copy.copy(occupiedPositions)

    while True:
        # occupiedPostionsの全ての要素を一つずつ下に落とす
        for i in range(len(occupiedPositions)):
            occupiedPositions[i] = (occupiedPositions[i][0], occupiedPositions[i][1] + 1)
        
        # 一つずつ下に落としたときに，その場所にミノが存在することができればドロップできていることになるのでcountをインクリメントする
        if isValidPlace(mainBoard, occupiedPositions):
            dropCount += 1
        else:
            break
    
    return dropCount
