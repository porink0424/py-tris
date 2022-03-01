from lib.classes import *

# directedMinoをmainBoardに埋め込む
def JoinDirectedMinoToBoard (directedMino:DirectedMino, board:Board):
    copiedBoard = copy.deepcopy(board)
    occupiedPositions = GetOccupiedPositions(directedMino)
    for position in occupiedPositions:
        if 0 <= position[1] < BOARD_HEIGHT:
            copiedBoard.mainBoard[position[1]][position[0]] = directedMino.mino
    
    return copiedBoard

# directedMinoをmainBoardに埋め込む
# 埋め込んだ結果は引数のboardに反映される。
def JoinDirectedMinoToBoard_uncopy (directedMino:DirectedMino, board:Board):
    occupiedPositions = GetOccupiedPositions(directedMino)
    for position in occupiedPositions:
        if 0 <= position[1] < BOARD_HEIGHT:
            board.mainBoard[position[1]][position[0]] = directedMino.mino

# directedMinoをmainBoardから外す
# 外した結果は引数のboardに反映される
def RemoveDirectedMinoFromBoard_uncopy (directedMino:DirectedMino, board:Board):
    occupiedPositions = GetOccupiedPositions(directedMino)
    for position in occupiedPositions:
        if 0 <= position[1] < BOARD_HEIGHT:
            board.mainBoard[position[1]][position[0]] = MINO.NONE
 