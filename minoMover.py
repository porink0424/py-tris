from lib import *
import decisionMaker

# directedMinoをboard上でmoveに従って動かす処理を行い，その動いた先のdirectedMinoを返す
# 注意；ここで与えられるmoveは正当であることがなんらかの方法で確認されているものとする。valid checkは行わない
def MoveOneStep (move:MOVE, directedMino:DirectedMino, board:Board) -> DirectedMino:
    if move is MOVE.LEFT:
        return DirectedMino(
            directedMino.mino,
            directedMino.direction,
            (directedMino.pos[0] - 1, directedMino.pos[1])
        )
    elif move is MOVE.RIGHT:
        return DirectedMino(
            directedMino.mino,
            directedMino.direction,
            (directedMino.pos[0] + 1, directedMino.pos[1])
        )
    elif move is MOVE.DOWN:
        return DirectedMino(
            directedMino.mino,
            directedMino.direction,
            (directedMino.pos[0], directedMino.pos[1] + 1)
        )
    elif move is MOVE.DROP:
        dropCount = decisionMaker.Drop(board.mainBoard, directedMino)
        return DirectedMino(
            directedMino.mino,
            directedMino.direction,
            (directedMino.pos[0], directedMino.pos[1] + dropCount)
        )
    elif move is MOVE.R_ROT or move is MOVE.L_ROT:
        return decisionMaker.Rotate(directedMino, move, board.mainBoard)
    else:
        Error("Invalid kind of moves.")
