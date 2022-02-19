from lib.classes import *

# mainBoard内で横一列が揃っている場合にそれを除去して，何ライン除去したかという情報と共に返す
def ClearLines(mainBoard:List[List[MINO]]) -> Tuple[List[List[MINO]], int]:
    # クリアされたrowのインデックスを保存していく
    clearedRowIdx = set()
    for i in range(len(mainBoard)):
        # 横一列が揃っているかチェック
        canClearLine = True
        for mino in mainBoard[i]:
            if mino is MINO.NONE:
                canClearLine = False
                break
        if canClearLine:
            clearedRowIdx.add(i)

    # clearedRowIdxに入っている行を実際に削除する
    newMainBoard = [[MINO.NONE for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    for i in range(BOARD_HEIGHT):
        if i not in clearedRowIdx:
            newMainBoard.append(mainBoard[i])
    
    return newMainBoard[(-BOARD_HEIGHT):], len(clearedRowIdx)
