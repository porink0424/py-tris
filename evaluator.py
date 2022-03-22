from lib import *
from params.eval import *

# 盤面自体の評価関数
def EvalMainBoard (mainBoard:List[int], topRowIdx:List[int]) -> float:
    # 凸凹具合を見る
    # 前の列との差分をみて，その差分の合計を凸凹具合とする
    
    # 各列において，上から順に見ていって，一番最初にブロックがある部分のrowIdxを格納する
    roughness = 0
    for i in range(len(topRowIdx) - 1):
        roughness += EVAL_ROUGHNESS_VAL[abs(topRowIdx[i] - topRowIdx[i+1])]

    # ブロックの下にある空白をカウントする
    # T-spinをさせるためにブロックの下にあるがT-spinできそうなところはカウントしない
    blankUnderBlock = 0
    continuousBlank = 0
    colBlockCount = 0
    for colIdx in range(BOARD_WIDTH):
        for rowIdx in range(topRowIdx[colIdx], BOARD_HEIGHT):
            # ブロックがある
            if mainBoard[rowIdx] & (0b1000000000 >> colIdx) != 0:
                colBlockCount += 1
                continuousBlank = 0
                continue
            
            if continuousBlank == 0:
                continuousBlank = 1

                # 上にブロックが2個以上あるときはダメ
                if colBlockCount >= 2:
                    blankUnderBlock += 1
                    continue

                # 隣の高さはこのマスより低い
                if ((colIdx - 1 >= 0 and rowIdx < topRowIdx[colIdx - 1]) and 
                    (colIdx - 2 >= 0 and mainBoard[rowIdx] & (0b1000000000 >> (colIdx - 2)) == 0)):
                    continue

                # 隣の高さはこのマスより低い
                if ((colIdx + 1 < BOARD_WIDTH and rowIdx < topRowIdx[colIdx + 1]) and 
                    (colIdx + 2 < BOARD_WIDTH and mainBoard[rowIdx] & (0b1000000000 >> (colIdx + 2)) == 0)):
                    continue
                
                # 空白を見つけた時は
                # その上にあるブロックの数だけ、評価値に影響を与えることにする。
                blankUnderBlock += colBlockCount
            else:
                # 空白を見つけた時は
                # その上にあるブロックの数だけ、評価値に影響を与えることにする。
                blankUnderBlock += colBlockCount

        continuousBlank = 0
        colBlockCount = 0
    
    topRowIdxSorted = copy.copy(topRowIdx)
    topRowIdxSorted.sort()
    # 盤面の高さを見る
    height = BOARD_HEIGHT - topRowIdxSorted[0]
    
    # 高さが一番低い列が他の列に対して3以上の高さの差がある、かつブロックの下に隙間がない時、
    # テトリスできる可能性が高い。
    tetris = 0
    if abs(topRowIdxSorted[-1] - topRowIdxSorted[-2]) >= 3 and blankUnderBlock == 0:
        tetris = EVAL_TETRIS_PATTERN
    
    # 高さが10以上のときはラインを消すことを最優先にしてもらう。
    heightEval = 0
    if height >= 10:
        heightEval += height * EVAL_HEIGHT_UPPER_THAN10
    elif height >= 5:
        heightEval += height * EVAL_HEIGHT_UPPER_THAN5
    elif height >= 1:
        heightEval += height * EVAL_HEIGHT
    else:
        heightEval += EVAL_PERFECT_CLEAR
    
    return tetris + heightEval + roughness * EVAL_ROUGHNESS + blankUnderBlock * EVAL_BLANK_UNDER_BLOCK

# Tスピンの判定
def IsTSpin (joinedMainBoard:List[int], directedMino:DirectedMino, moveList:List[MoveInt]) -> bool:
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
def IsTSpinMini (joinedMainBoard:List[int], directedMino:DirectedMino, moveList:List[MoveInt]) -> bool:
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
def EvalPath (moveList:List[MoveInt], clearedRowCount:int, joinedMainBoard:List[int], directedMino:DirectedMino, backToBack:bool, ren:int) -> float:
    t_spin = 0
    isBackToBack = False 

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
        isBackToBack = True
    
    if clearedRowCount == 4:
        isBackToBack = True

    isBackToBack = isBackToBack and backToBack

    eval = t_spin + \
           EVAL_LINE_CLEAR[clearedRowCount] + \
           (EVAL_BACKTOBACK if isBackToBack else 0) + \
           EVAL_REN[ren]
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
    nextBackToBack = isTspinOrTetris or (backToBack and clearedRowCount == 0)
    return score, nextBackToBack, ren
