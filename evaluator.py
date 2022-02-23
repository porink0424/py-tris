from lib import *
from params.eval import *

# 盤面自体の評価関数
def EvalMainBoard (mainBoard) -> float:
    # 凸凹具合を見る
    # 前の列との差分をみて，その差分の合計を凸凹具合とする

    # 各列において，上から順に見ていって，一番最初にブロックがある部分のrowIdxを格納する
    topRowIdx = []
    for colIdx in range(BOARD_WIDTH):
        isFound = False
        for rowIdx in range(BOARD_HEIGHT):
            if mainBoard[rowIdx][colIdx] is not MINO.NONE:
                topRowIdx.append(rowIdx)
                isFound = True
                break
        if not isFound:
            topRowIdx.append(BOARD_HEIGHT)
    roughness = 0
    for i in range(len(topRowIdx) - 1):
        roughness += abs(topRowIdx[i] - topRowIdx[i+1])

    # ブロックの下にある空白をカウントする
    blankUnderBlock = 0
    for colIdx in range(BOARD_WIDTH):
        for rowIdx in range(topRowIdx[colIdx], BOARD_HEIGHT):
            if mainBoard[rowIdx][colIdx] is MINO.NONE:
                blankUnderBlock += 1
    
    return roughness * EVAL_ROUGHNESS + blankUnderBlock * EVAL_BLANK_UNDER_BLOCK


# 経路・ライン数の評価関数
def EvalPath (moveList:List[MOVE], clearedRowCount:int) -> float:
    # 今はmoveListは無視している
    return clearedRowCount * EVAL_LINE_CLEAR


def Eval(moveList:List[MOVE], board:Board, clearedRowCount:int) -> float:
    # ライン消去後の盤面自体の評価
    evalMainBoard = EvalMainBoard(board.mainBoard)

    # 経路の評価
    evalPath = EvalPath(moveList, clearedRowCount)

    return evalMainBoard + evalPath