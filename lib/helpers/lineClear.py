from lib.classes import *

# mainBoard内で横一列が揃っている場合にそれを除去して，何ライン除去したかという情報と共に返す
def ClearLines(mainBoard:List[int], topRowIdx:List[int]) -> Tuple[List[int], List[int], int]:
    # クリアされたrowのインデックスを保存していく
    clearedRowIdx = set()
    for i in range(BOARD_HEIGHT):
        # 横一列が揃っているかチェック
        if mainBoard[i] == 0b1111111111:
            clearedRowIdx.add(i)

    # clearedRowIdxに入っている行を実際に削除する
    newMainBoard = [0b0 for _ in range(BOARD_HEIGHT)]
    for i in range(BOARD_HEIGHT):
        if i not in clearedRowIdx:
            newMainBoard.append(mainBoard[i])

    newMainBoard = newMainBoard[(-BOARD_HEIGHT):]
    clearedRowCount = len(clearedRowIdx)
    newTopRowIdx = copy.copy(topRowIdx)

    for i in range(BOARD_WIDTH):
        for j in range(topRowIdx[i], BOARD_HEIGHT):
            if newMainBoard[j] & (0b1000000000 >> i) > 0:
                newTopRowIdx[i] = j
                break
            else:
                newTopRowIdx[i] = BOARD_HEIGHT
    
    return newMainBoard, newTopRowIdx, clearedRowCount

# mainBoard内で横一列が揃っている場合にそれを除去して，何ライン除去したかという情報と共に返す
# topRowIdxの処理はしない
def ClearLinesWithoutTopRowIdx(mainBoard:List[int]) -> Tuple[List[int], int]:
    # クリアされたrowのインデックスを保存していく
    clearedRowIdx = set()
    for i in range(BOARD_HEIGHT):
        # 横一列が揃っているかチェック
        if mainBoard[i] == 0b1111111111:
            clearedRowIdx.add(i)

    # clearedRowIdxに入っている行を実際に削除する
    newMainBoard = [0b0 for _ in range(BOARD_HEIGHT)]
    for i in range(BOARD_HEIGHT):
        if i not in clearedRowIdx:
            newMainBoard.append(mainBoard[i])

    newMainBoard = newMainBoard[(-BOARD_HEIGHT):]
    clearedRowCount = len(clearedRowIdx)
    
    return newMainBoard, clearedRowCount

# mainBoard内で横一列が揃っている場合に、何ライン除去したかという情報を返す。
# 実際に変更はしない
def ClearLinesCalc(mainBoard:List[List[MINO]]) -> int:
    # クリアされたrowのインデックスを保存していく
    clearedRowCnt = 0
    for row in mainBoard:
        # 横一列が揃っているかチェック
        if row == 0b1111111111:
            clearedRowCnt += 1
        
    return clearedRowCnt
