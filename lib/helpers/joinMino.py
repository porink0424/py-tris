from lib.classes import *

# directedMinoをmainBoardに埋め込む
def JoinDirectedMinoToBoard (directedMino:DirectedMino, mainBoard:List[int], topRowIdx:List[int]) -> Tuple[List[int], List[int]]:
    copiedMainBoard = copy.copy(mainBoard)
    copiedTopRowIdx = copy.copy(topRowIdx) 
    occupiedPositions = GetOccupiedPositions(directedMino)
    for pos0, pos1 in occupiedPositions:
        assert 0 <= pos1 < BOARD_HEIGHT
        copiedMainBoard[pos1] |= (0b1000000000 >> pos0)
        copiedTopRowIdx[pos0] = min(copiedTopRowIdx[pos0], pos1)
    
    return copiedMainBoard, copiedTopRowIdx

# directedMinoをmainBoardに埋め込む
# topRowIdxの処理はしない
def JoinDirectedMinoToBoardWithoutTopRowIdx (directedMino:DirectedMino, mainBoard:List[int]) -> List[int]:
    copiedMainBoard = copy.copy(mainBoard)
    occupiedPositions = GetOccupiedPositions(directedMino)
    for pos0, pos1 in occupiedPositions:
        assert 0 <= pos1 < BOARD_HEIGHT
        copiedMainBoard[pos1] |= (0b1000000000 >> pos0)
    
    return copiedMainBoard

# directedMinoをmainBoardに埋め込む
# 埋め込んだ結果は引数のboardとtopRowIdxに反映される。
def JoinDirectedMinoToBoardUncopy (directedMino:DirectedMino, mainBoard:List[int], topRowIdx:List[int]):
    occupiedPositions = GetOccupiedPositions(directedMino)
    for pos0, pos1 in occupiedPositions:
        assert 0 <= pos1 < BOARD_HEIGHT
        mainBoard[pos1] |= (0b1000000000 >> pos0)
        topRowIdx[pos0] = min(topRowIdx[pos0], pos1)

 
