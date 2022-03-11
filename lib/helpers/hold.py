from lib.classes import *

def BoardAfterHold(board:Board) -> Board:
    if board.holdMino is MINO.NONE:
        return Board(
            board.mainBoard,
            DirectedMino(
                board.followingMinos[0],
                FIRST_MINO_DIRECTION,
                FIRST_MINO_POS,
            ),
            board.followingMinos[1:] + [MINO.NONE],
            board.currentMino.mino,
            False, # いらないかも
            board.topRowIdx,
            board.score,
            board.backToBack,
            board.ren,
            board.minoBagContents
        )
    else:
        return Board(
            board.mainBoard,
            DirectedMino(
                board.holdMino,
                FIRST_MINO_DIRECTION,
                FIRST_MINO_POS
            ),
            board.followingMinos,
            board.currentMino.mino,
            False, # いらないかも
            board.topRowIdx,
            board.score,
            board.backToBack,
            board.ren,
            board.minoBagContents
        )