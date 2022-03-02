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

# directedMinoがmoveをしたときに、directedMinoの中心がどこに移動するかを返す
def GetMovedDirectedMinoPos (move:MOVE, directedMino:DirectedMino) -> Tuple[int]:
    pos = directedMino.pos
    if move is MOVE.LEFT:
        return (pos[0]-1, pos[1])
    elif move is MOVE.RIGHT:
        return (pos[0]+1,                   ここから          )

# moveListとdirectedMinoを受け取って、その通りに入力を行う
# moveList = [downが入っていないmove1] + [downの連続列] + [downが入っていないmove2]の形のみに対応している
# todo: より一般的なmoveListに対しても動くようにする
def InputMove (moveList:List[MOVE], directedMino:DirectedMino) -> None:
    # moveList = [move1] + [downの連続列] + [move2]に分割する
    if MOVE.DOWN in moveList:
        downStartIdx = 0
        while True:
            if moveList[downStartIdx] is MOVE.DOWN:
                break
            else:
                downStartIdx += 1
        downEndIdx = len(moveList)
        while True:
            if moveList[downEndIdx-1] is MOVE.DOWN:
                break
            else:
                downEndIdx -= 1
        move1 = moveList[:downStartIdx]
        down = moveList[downStartIdx:downEndIdx]
        move2 = moveList[downEndIdx:]
    else:
        move1 = moveList
        down = []
        move2 = []
    
    # move1を入力
    for move in move1:
        Move(move)
        GetMovedDirectedMinoPosをつかってposを追う
    
    # 
