from lib.classes import *
from lib.helpers.check import isValidPlace

# 受け取ったdirectedMinoをいけるところまで下に落とす。何個分おとせるかを返す
def Drop(mainBoard:List[int], directedMino:DirectedMino) -> int:
    dropCount = 0
    occupiedPositions = GetOccupiedPositions(directedMino)

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
