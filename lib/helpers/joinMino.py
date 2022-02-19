from lib.classes import *

# directedMinoをmainBoardに埋め込む
def JoinDirectedMinoToBoard (directedMino:DirectedMino, board:Board):
    copiedBoard = copy.deepcopy(board)
    occupiedPositions = GetOccupiedPositions(directedMino)
    for position in occupiedPositions:
        if 0 <= position[1] < BOARD_HEIGHT:
            copiedBoard.mainBoard[position[1]][position[0]] = directedMino.mino
    
    return copiedBoard
