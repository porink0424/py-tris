from lib import *
from params.eval import *

# 盤面自体の評価関数
# mainBoardはミノを埋め込んだだけでまだRowを消していない盤面
def EvalMainBoard (mainBoard, cleardRowCount:int, topRowIdx:List[int], evalParam:Evalparam) -> float:
    # 凸凹具合を見る
    # 前の列との差分をみて，その差分の合計を凸凹具合とする
    
    # 各列において，上から順に見ていって，一番最初にブロックがある部分のrowIdxを格納する
    roughness = 0
    for i in range(len(topRowIdx) - 1):
        roughness += abs(topRowIdx[i] - topRowIdx[i+1])

    # ブロックの下にある空白をカウントする
    blankUnderBlock = 0
    for colIdx in range(BOARD_WIDTH):
        for rowIdx in range(topRowIdx[colIdx] + cleardRowCount, BOARD_HEIGHT):
            if mainBoard[rowIdx] & (0b1000000000 >> colIdx) == 0:
                blankUnderBlock += 1
    
    # 盤面の高さを見る
    minTopRowIdx = BOARD_HEIGHT
    for idx in topRowIdx:
        minTopRowIdx = min(minTopRowIdx, idx)
    height = BOARD_HEIGHT - minTopRowIdx - cleardRowCount

    eval = 0
    if height >= 10:
        eval += height * (evalParam.EVAL_HEIGHT - 100000)
    else:
        eval += height * evalParam.EVAL_HEIGHT
    
    return eval + roughness * evalParam.EVAL_ROUGHNESS + blankUnderBlock * evalParam.EVAL_BLANK_UNDER_BLOCK

# Tスピンの判定
def IsTSpin (joinedMainBoard:List[int], directedMino:DirectedMino, moveList:List[MOVE]) -> bool:
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
    pos0, pos1 = directedMino.pos
    if pos0 - 1 < 0 or pos1 - 1 < 0 or joinedMainBoard[pos1-1] & (0b1000000000 >> (pos0-1)) > 0: # 左上
        count += 1
    if pos0 - 1 < 0 or pos1 + 1 >= BOARD_HEIGHT or joinedMainBoard[pos1+1] & (0b1000000000 >> (pos0-1)) > 0: # 左下
        count += 1
    if pos0 + 1 >= BOARD_WIDTH or pos1 + 1 >= BOARD_HEIGHT or joinedMainBoard[pos1+1] & (0b1000000000 >> (pos0+1)) > 0: # 右下
        count += 1
    if pos0 + 1 >= BOARD_WIDTH or pos1 - 1 < 0 or joinedMainBoard[pos1-1] & (0b1000000000 >> (pos0+1)) > 0: # 右上
        count += 1
    if count <= 2:
        return False

    # ②の判定
    if moveList[-1] is MOVE.DROP:
        if len(moveList) < 2: # DROPしかないので最後が回転ではない
            return False
        if moveList[-2] is not MOVE.L_ROT and moveList[-2] is not MOVE.R_ROT: # L_ROTでもR_ROTでもない場合は最後が回転ではない
            return False
        if MOVE.DOWN not in moveList: # ただのROT→DROPというようなmoveListを除く
            return False
    else:
        Error("Invalid MoveList from IsTSpin.")

    return True

# Tスピン-miniであるかどうかの判定
# Tスピンであることは前提として判定を省略する
def IsTSpinMini (joinedMainBoard:List[int], directedMino:DirectedMino, moveList:List[MOVE]) -> bool:
    """
    T-Spin Miniの判定条件
    ①T-Spinの条件を満たしていること
    ②ミノ固定時のTミノの4隅のうち，凸側の1つが空いていること
    ③SRSにおける回転補正の4番目(回転中心移動が(±1, ±2))でないこと
    """

    # ②の判定
    pos0, pos1 = directedMino.pos
    if directedMino.direction is DIRECTION.N:
        if (
            (pos0 - 1 < 0 or pos1 - 1 < 0 or joinedMainBoard[pos1-1] & (0b1000000000 >> (pos0-1)) > 0) and # 左上が空いていない
            (pos0 + 1 >= BOARD_WIDTH or pos1 - 1 < 0 or joinedMainBoard[pos1-1] & (0b1000000000 >> (pos0+1)) > 0) # 右上が空いていない
        ):
            return False
    elif directedMino.direction is DIRECTION.E:
        if (
            (pos0 + 1 >= BOARD_WIDTH or pos1 + 1 >= BOARD_HEIGHT or joinedMainBoard[pos1+1] & (0b1000000000 >> (pos0+1)) > 0) and # 右下が空いていない
            (pos0 + 1 >= BOARD_WIDTH or pos1 - 1 < 0 or joinedMainBoard[pos1-1] & (0b1000000000 >> (pos0+1)) > 0) # 右上が空いていない
        ):
            return False
    elif directedMino.direction is DIRECTION.S:
        if (
            (pos0 + 1 >= BOARD_WIDTH or pos1 + 1 >= BOARD_HEIGHT or joinedMainBoard[pos1+1] & (0b1000000000 >> (pos0+1)) > 0) and # 右下が空いていない
            (pos0 - 1 < 0 or pos1 + 1 >= BOARD_HEIGHT or joinedMainBoard[pos1+1] & (0b1000000000 >> (pos0-1)) > 0) # 左下が空いていない
        ):
            return False
    else:
        if (
            (pos0 - 1 < 0 or pos1 - 1 < 0 or joinedMainBoard[pos1-1] & (0b1000000000 >> (pos0-1)) > 0) and # 左上が空いていない
            (pos0 - 1 < 0 or pos1 + 1 >= BOARD_HEIGHT or joinedMainBoard[pos1+1] & (0b1000000000 >> (pos0-1)) > 0) # 左下が空いていない
        ):
            return False
    
    # ③の判定
    lastRotate = moveList[-2] # DROPの前の最後の回転を取得
    reversedLastRotate = MOVE.R_ROT if lastRotate is MOVE.L_ROT else MOVE.L_ROT
    # joinedMainBoardからdirectedMinoの部分のブロックを消去
    occupiedPositions = GetOccupiedPositions(directedMino)
    deletedMainBoard = copy.copy(joinedMainBoard)
    for pos0, pos1 in occupiedPositions:
        deletedMainBoard[pos1] &= 0b1111111111 ^ (0b1000000000 >> pos0)
    # 回転補正が4番目であるならMiniではない
    if GetRotateNum(directedMino, reversedLastRotate, deletedMainBoard) == 4:
        return False
    
    return True

# 経路・ライン数の評価関数
def EvalPath (moveList:List[MOVE], clearedRowCount:int, joinedMainBoard:List[int], directedMino:DirectedMino, evalparam:Evalparam, backtoback:bool, ren:int) -> float:
    t_spin = 0
    isbtb = False 

    if IsTSpin(joinedMainBoard, directedMino, moveList):
        if IsTSpinMini(joinedMainBoard, directedMino, moveList):
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
        isbtb = True
    
    if clearedRowCount == 4:
        isbtb = True

    isbtb = isbtb and backtoback

    eval = t_spin + \
           evalparam.EVAL_LINE_CLEAR[clearedRowCount] + \
           (evalparam.EVAL_BACKTOBACK if isbtb else 0) + \
           evalparam.EVAL_REN[ren]
    return eval

def Score(isTspin:bool, isTspinmini:bool, clearedRowCount:int, backToBack:bool, ren:int) -> Tuple[int, bool, int]:
    score = 0
    isTspinOrTetris = False

    if isTspin:
        if isTspinmini:
            score += SCORE_T_SPIN_MINI
        else:
            if clearedRowCount == 1:
                score += SCORE_T_SPIN_SINGLE
            elif clearedRowCount == 2:
                score += SCORE_T_SPIN_DOUBLE
            elif clearedRowCount == 3:
                score += SCORE_T_SPIN_TRIPLE
        isTspinOrTetris = True

    if clearedRowCount == 1:
        score += SCORE_SINGLE
        ren += 1
    elif clearedRowCount == 2:
        score += SCORE_DOUBLE
        ren += 1
    elif clearedRowCount == 3:
        score += SCORE_TRIPLE
        ren += 1
    elif clearedRowCount == 4:
        score += SCORE_TETRIS
        ren += 1
        isTspinOrTetris = True
    elif clearedRowCount == 0:
        ren = 0

    if backToBack and isTspinOrTetris:
        score += 1

    score += SCORE_REN[ren]
    return score, isTspinOrTetris, ren

    

    