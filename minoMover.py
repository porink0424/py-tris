from lib import *
import decisionMaker
import boardWatcher

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

# directedMinoがmoveをしたときに、directedMinoがどこに移動するかを返す
def GetMovedDirectedMino (move:MOVE, directedMino:DirectedMino, mainBoard:List[int]) -> DirectedMino:
    pos = directedMino.pos
    if move is MOVE.LEFT:
        return DirectedMino(directedMino.mino, directedMino.direction, (pos[0]-1, pos[1]))
    elif move is MOVE.RIGHT:
        return DirectedMino(directedMino.mino, directedMino.direction, (pos[0]+1, pos[1]))
    elif move is MOVE.DOWN:
        return DirectedMino(directedMino.mino, directedMino.direction, (pos[0], pos[1]+1))
    elif move is MOVE.DROP:
        return DirectedMino(directedMino.mino, directedMino.direction, (pos[0], pos[1]+Drop(mainBoard, directedMino)))
    elif move is MOVE.L_ROT or move is MOVE.R_ROT:
        return Rotate(directedMino, move, mainBoard)
    else:
        Error("Invalid move from GetMovedDirectedMinoPos")

# moveListとdirectedMinoを受け取って、その通りに入力を行う
# moveList = [downが入っていないmove1] + [downの連続列] + [downが入っていないmove2]の形のみに対応している
# directedMinoをmoveListに従って動かした結果の移動先のdirectedMinoを返す
# todo: より一般的なmoveListに対しても動くようにする
def InputMove (moveList:List[MOVE], directedMino:DirectedMino, mainBoard:List[int]) -> DirectedMino:
    pos = directedMino.pos
    nextDirectedMino = directedMino

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
        downCount = len(moveList[downStartIdx:downEndIdx])
        move2 = moveList[downEndIdx:]
    else:
        move1 = moveList
        downCount = 0
        move2 = []

    # move1を入力
    for move in move1:
        Move(move)
        nextDirectedMino = GetMovedDirectedMino(move, nextDirectedMino, mainBoard)
    
    # downを入力
    if downCount > 0:
        HoldDown() # 目的の場所にたどり着くまで下を押し続ける
        nextDirectedMino = DirectedMino(nextDirectedMino.mino, nextDirectedMino.direction, (nextDirectedMino.pos[0], nextDirectedMino.pos[1] + downCount))
        occupiedPositions = GetOccupiedPositions(nextDirectedMino)
        while True:
            hasReached = True
            for pos in occupiedPositions:
                pos = (pos[0], pos[1] - (BOARD_HEIGHT - DISPLAYED_BOARD_HEIGHT))
                if boardWatcher.GetPixelColor(pos) is not nextDirectedMino.mino:
                    hasReached = False
                    break
            if hasReached:
                ReleaseDown()
                break
    
    # move2を入力
    for move in move2:
        Move(move)
        nextDirectedMino = GetMovedDirectedMino(move, nextDirectedMino, mainBoard)

    return nextDirectedMino
