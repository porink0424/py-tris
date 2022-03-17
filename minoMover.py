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
# moveList = [downが入っていないfirstHalfMove] + [downの連続列] + [downが入っていないsecondHalfMove]の形のみに対応している
# directedMinoをmoveListに従って動かした結果の移動先のdirectedMinoを返す
# 置きミスしたときは、Noneを返す
# todo: より一般的なmoveListに対しても動くようにする
def InputMove (moveList:List[MOVE], directedMino:DirectedMino, mainBoard:List[int]) -> Union[DirectedMino, bool]:
    nextDirectedMino = directedMino

    # moveList = [firstHalfMove] + [downの連続列] + [secondHalfMove]に分割する
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
        firstHalfMove = moveList[:downStartIdx]
        downCount = len(moveList[downStartIdx:downEndIdx])
        secondHalfMove = moveList[downEndIdx:]
    else:
        firstHalfMove = moveList
        downCount = 0
        secondHalfMove = []

    # firstHalfMoveを入力
    for move in firstHalfMove:
        Move(move)
        nextDirectedMino = GetMovedDirectedMino(move, nextDirectedMino, mainBoard)
    
    # downを入力
    if downCount > 0:
        HoldDown() # 目的の場所にたどり着くまで下を押し続ける
        nextDirectedMino = DirectedMino(nextDirectedMino.mino, nextDirectedMino.direction, (nextDirectedMino.pos[0], nextDirectedMino.pos[1] + downCount))
        count = 0
        posNotChangeCount = 0
        previousPosYOfCurrentMino = boardWatcher.GetPosOfCurrentMino()[1]
        while True:
            # 下ボタンを押してるにもかかわらず位置が変わっていない場合
            if previousPosYOfCurrentMino == boardWatcher.GetPosOfCurrentMino()[1]:
                posNotChangeCount += 1
                if posNotChangeCount > 18: # 0.18秒程度押し続けても変わらない場合到達していると考えられる
                    ReleaseDown()
                    break
            previousPosYOfCurrentMino = boardWatcher.GetPosOfCurrentMino()[1]
            count += 1
            # 回転入れがある程度の時間成功しない時は失敗とみなす todo: もっといい方法はないか
            if count > 200:
                ReleaseDown()
                return None

            time.sleep(0.01)
    
    # secondHalfMoveを入力
    for move in secondHalfMove:
        Move(move)
        nextDirectedMino = GetMovedDirectedMino(move, nextDirectedMino, mainBoard)

    return nextDirectedMino
