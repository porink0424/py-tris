from lib.classes import *

# directedMinoをmainBoardに埋め込む
def JoinDirectedMinoToBoard (directedMino:DirectedMino, mainBoard:List[int]) -> List[int]:
    copiedMainBoard = copy.copy(mainBoard)
    occupiedPositions = GetOccupiedPositions(directedMino)
    for position in occupiedPositions:
        if 0 <= position[1] < BOARD_HEIGHT:
            copiedMainBoard[position[1]] |= (0b1000000000 >> position[0])
    
    return copiedMainBoard
