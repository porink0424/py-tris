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

# Tスピンの判定
def IsTSpin (joinedMainBoard, directedMino:DirectedMino, moveList:List[MOVE]) -> bool:
    """
    T-Spinの判定条件
    ①ミノ固定時にTミノの4隅が3つ以上埋まっていること
    ②最後の動作が回転であること
    """

    # 前提条件：directedMinoがTミノであること
    if directedMino.mino is not MINO.T:
        return False

    # ①の判定
    count = 0
    pos = directedMino.pos
    if pos[0] - 1 < 0 or pos[1] - 1 < 0 or joinedMainBoard[pos[1]-1][pos[0]-1] is not MINO.NONE: # 左上
        count += 1
    if pos[0] - 1 < 0 or pos[1] + 1 >= BOARD_HEIGHT or joinedMainBoard[pos[1]+1][pos[0]-1] is not MINO.NONE: # 左下
        count += 1
    if pos[0] + 1 >= BOARD_WIDTH or pos[1] + 1 >= BOARD_HEIGHT or joinedMainBoard[pos[1]+1][pos[0]+1] is not MINO.NONE: # 右下
        count += 1
    if pos[0] + 1 >= BOARD_WIDTH or pos[1] - 1 < 0 or joinedMainBoard[pos[1]-1][pos[0]+1] is not MINO.NONE: # 右上
        count += 1
    if count <= 2:
        return False

    # ②の判定
    if moveList[-1] is MOVE.DROP:
        if len(moveList) < 2: # DROPしかないので最後が回転ではない
            return False
        elif moveList[-2] is not MOVE.L_ROT and moveList[-2] is not MOVE.R_ROT: # L_ROTでもR_ROTでもない場合は最後が回転ではない
            return False
    else:
        Error("Invalid MoveList from IsTSpin.")

    return True

# Tスピン-miniであるかどうかの判定
# Tスピンであることは前提として判定を省略する
def IsTSpinMini () -> bool:
    """
    T-Spin Miniの判定条件
    ①T-Spinの条件を満たしていること
    ②ミノ固定時のTミノの4隅のうち，凸側の1つが空いていること
    ③SRSにおける回転補正の4番目(回転中心移動が(±1, ±2))でないこと
    """

    # todo: 実装
    return False

# 経路・ライン数の評価関数
def EvalPath (moveList:List[MOVE], clearedRowCount:int, joinedMainBoard, directedMino:DirectedMino) -> float:
    t_spin = 0
    if IsTSpin(joinedMainBoard, directedMino, moveList):
        if IsTSpinMini():
            if clearedRowCount == 1:
                t_spin = EVAL_T_SPIN_MINI_SINGLE
            elif clearedRowCount == 2:
                t_spin = EVAL_T_SPIN_MINI_DOUBLE
        else:
            if clearedRowCount == 1:
                t_spin = EVAL_T_SPIN_SINGLE
            elif clearedRowCount == 2:
                t_spin = EVAL_T_SPIN_DOUBLE
            elif clearedRowCount == 3:
                t_spin = EVAL_T_SPIN_TRIPLE
    
    return t_spin + EVAL_LINE_CLEAR[clearedRowCount]
