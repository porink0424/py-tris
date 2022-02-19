from lib import *
import minoMover

DISPLAY_DELTA_TIME = 0.2

# 1つのnowDirectedMinoを置く動きを再現して出力
# 返り値としておいた後のboardを返す
def PutMino (moveList:List[MOVE], nowDirectedMino:DirectedMino, board:Board) -> Board:
    # moveListに従って1つずつ動かしていく
    nextDirectedMino = nowDirectedMino
    for move in moveList:
        PrintBoardWithColorWithDirectedMino(board, nextDirectedMino, True)
        nextDirectedMino = minoMover.MoveOneStep(move, nextDirectedMino, board)
        time.sleep(DISPLAY_DELTA_TIME)
    
    # 最終状態の出力
    PrintBoardWithColorWithDirectedMino(board, nextDirectedMino, True)

    return JoinDirectedMinoToBoard(nextDirectedMino, board)
