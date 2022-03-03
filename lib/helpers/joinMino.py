from lib.classes import *

# directedMinoをmainBoardに埋め込む
def JoinDirectedMinoToBoard (directedMino:DirectedMino, mainBoard:List[int]) -> List[int]:
    copiedMainBoard = copy.copy(mainBoard)
    occupiedPositions = GetOccupiedPositions(directedMino)
    for pos0, pos1 in occupiedPositions:
        if 0 <= pos1 < BOARD_HEIGHT:
            copiedMainBoard[pos1] |= (0b1000000000 >> pos0)
    
    return copiedMainBoard

# directedMinoをmainBoardに埋め込む
# 埋め込んだ結果は引数のboardに反映される。
def JoinDirectedMinoToBoard_uncopy (directedMino:DirectedMino, mainBoard:List[int]):
    occupiedPositions = GetOccupiedPositions(directedMino)
    for pos0, pos1 in occupiedPositions:
        if 0 <= pos1 < BOARD_HEIGHT:
            mainBoard[pos1] |= (0b1000000000 >> pos0)

# directedMinoをmainBoardから外す
# 外した結果は引数のboardに反映される
def RemoveDirectedMinoFromBoard_uncopy (directedMino:DirectedMino, mainBoard:List[int]):
    occupiedPositions = GetOccupiedPositions(directedMino)
    for pos0, pos1 in occupiedPositions:
        if 0 <= pos1 < BOARD_HEIGHT:
            mainBoard[pos1] &= (0b1111111111 ^ (0b1000000000 >> pos0))
 
