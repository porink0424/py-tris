from lib.classes import *

# directedMinoをmainBoardから消去する
def DeleteDirectedMinoFromMainBoard (directedMino:DirectedMino, mainBoard:List[int], topRowIdx:List[int]) -> Tuple[List[int], List[int]]:
    copiedMainBoard = copy.copy(mainBoard)
    copiedTopRowIdx = copy.copy(topRowIdx)
    occupiedPositions = GetOccupiedPositions(directedMino)
    for pos0, pos1 in occupiedPositions:
        assert 0 <= pos1 < BOARD_HEIGHT
        copiedMainBoard[pos1] &= 0b1111111111 ^ (0b1000000000 >> pos0)
        if copiedTopRowIdx[pos0] == pos1:
            for rowIdx in range(pos1, BOARD_HEIGHT):
                if copiedMainBoard[rowIdx] & (0b1000000000 >> pos0) > 0:
                    copiedTopRowIdx[pos0] = rowIdx
                    break
            else:
                copiedTopRowIdx[pos0] = BOARD_HEIGHT
        else:
            assert copiedTopRowIdx[pos0] < pos1
    
    return copiedMainBoard, copiedTopRowIdx

# directedMinoをmainBoardから外す
# 外した結果は引数のboardとtopRowIdxに反映される
def DeleteDirectedMinoFromBoardUncopy (directedMino:DirectedMino, mainBoard:List[int], topRowIdx:List[int]):
    occupiedPositions = GetOccupiedPositions(directedMino)
    for pos0, pos1 in occupiedPositions:
        assert 0 <= pos1 < BOARD_HEIGHT
        mainBoard[pos1] &= (0b1111111111 ^ (0b1000000000 >> pos0))
        if topRowIdx[pos0] == pos1:
            for rowIdx in range(pos1, BOARD_HEIGHT):
                if mainBoard[rowIdx] & (0b1000000000 >> pos0) > 0:
                    topRowIdx[pos0] = rowIdx
                    break
            else:
                topRowIdx[pos0] = BOARD_HEIGHT
        else:
            assert topRowIdx[pos0] < pos1
