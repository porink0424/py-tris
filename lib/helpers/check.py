from lib.classes import *

# 占有しようとしている場所がちゃんと空白になっているかチェックする
def isValidPlace(mainBoard, occupiedPositions:List[Tuple[int]]) -> bool:
    for place in occupiedPositions:
        # 盤面の左右の外にはみ出ていないこと
        if not 0 <= place[0] < BOARD_WIDTH:
            return False
        # 盤面の上下の外にはみ出ていないこと
        if not 0 <= place[1] < BOARD_HEIGHT:
            return False
        # placeの場所が空白であること
        if mainBoard[place[1]][place[0]] is not MINO.NONE:
            return False
    
    return True

# おこうとしている位置のどこかのブロックの下にちゃんと既存のブロックがあって，おくことができる場所であるかをチェックする
def CanPut(mainBoard, occupiedPositions:List[Tuple[int]]) -> bool:
    for place in occupiedPositions:
        if place[1] + 1 < BOARD_HEIGHT and mainBoard[place[1]+1][place[0]] is not MINO.NONE:
            return True
        elif place[1] + 1 == BOARD_HEIGHT:
            return True
    return False