from lib.classes import *

# directedMinoをmainBoardに埋め込む
def JoinDirectedMinoToBoard (directedMino:DirectedMino, mainBoard:List[int]) -> List[int]:
    copiedMainBoard = copy.copy(mainBoard)
    occupiedPositions = GetOccupiedPositions(directedMino)
    for position in occupiedPositions:
        if 0 <= position[1] < BOARD_HEIGHT:
            copiedMainBoard[position[1]] |= (0b1000000000 >> position[0])
    
    return copiedMainBoard

# directedMinoをmainBoardに埋め込む
# 埋め込んだ結果は引数のboardに反映される。
def JoinDirectedMinoToBoard_uncopy (directedMino:DirectedMino, mainBoard:List[int]):
    occupiedPositions = GetOccupiedPositions(directedMino)
    for position in occupiedPositions:
        if 0 <= position[1] < BOARD_HEIGHT:
            mainBoard[position[1]] |= (0b1000000000 >> position[0])

# directedMinoをmainBoardから外す
# 外した結果は引数のboardに反映される
def RemoveDirectedMinoFromBoard_uncopy (directedMino:DirectedMino, mainBoard:List[int]):
    occupiedPositions = GetOccupiedPositions(directedMino)
    for position in occupiedPositions:
        if 0 <= position[1] < BOARD_HEIGHT:
            mainBoard[position[1]] &= (0b1111111111 ^ (0b1000000000 >> position[0]))
 
