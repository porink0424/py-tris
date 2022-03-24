from lib.classes import *

# 真上から光を照射した時に光が当たらず，かつ外部と連なっている空きマスを各連なりごとに返す
def findConnectedHiddenSpaces(board:Board) -> List[List[Tuple[int]]]:

    columnHasARoof = [False for _ in range(BOARD_WIDTH)]
    connectedHiddenSpaces = []
    for y,row in enumerate(board):
        for x,cell in row:
            if cell is not MINO.NONE:
                columnHasARoof[x] = True
            else:
                if columnHasARoof[x]:
                  pass # TODO
                  
                else:
                    continue
            
    return connectedHiddenSpaces

















# 屋根の下に隠れているような場所を探して座標の集合を返す
# 換言すると，真上から光を照射した時に光が当たらない空きマスを探す
def findHiddenSpace(board:Board) -> List[Tuple[int]] :

    hiddenSpaces = []
    for x in range(BOARD_WIDTH):
        currentColumnHaveARoof = False
        for y in range(BOARD_HEIGHT):
            if board[y][x] is not MINO.NONE:
                currentColumnHaveARoof = True
            else:
                if currentColumnHaveARoof:
                    hiddenSpaces.append((x,y))
                else:
                    continue

    return hiddenSpaces

# findHiddenSpace で見つかった空きマスのうち，１つだけで存在しているものを消した空きマス集合を返す
def removeIsolatedHiddenSpace(board:Board, hiddenSpaces:List[Tuple[int]]) -> List[Tuple[int]]:

    hiddenSpacesSet = set(hiddenSpaces)
    connectedHiddenSpacesSet = set()
    # 上下左右の順に，隣接するマスが hiddenSpaces に含まれるかみていく
    for (x,y) in hiddenSpaces:
        if y>0:
            if (x,y-1) in hiddenSpacesSet: # 上
                connectedHiddenSpacesSet.add((x,y))
                continue
        if y<BOARD_HEIGHT-1:
            if (x,y+1) in hiddenSpacesSet: # 下
                connectedHiddenSpacesSet.add((x,y))
                continue
        if x>0:
            if (x-1,y) in hiddenSpacesSet: # 左
                connectedHiddenSpacesSet.add((x,y))
                continue
        if x<BOARD_WIDTH-1:
            if (x+1,y) in hiddenSpacesSet: # 右
                connectedHiddenSpacesSet.add((x,y))
                continue

    return list(connectedHiddenSpacesSet)
