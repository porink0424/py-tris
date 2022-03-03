from lib.classes import *

# 占有しようとしている場所がちゃんと空白になっているかチェックする
def isValidPlace(mainBoard:List[int], occupiedPositions:List[Tuple[int]]) -> bool:
    for pos in occupiedPositions:
        # 盤面の左右の外にはみ出ていないこと
        if not 0 <= pos[0] < BOARD_WIDTH:
            return False
        # 盤面の上下の外にはみ出ていないこと
        if not 0 <= pos[1] < BOARD_HEIGHT:
            return False
        # posの場所が空白であること
        if mainBoard[pos[1]] & (0b1000000000 >> pos[0]) > 0:
            return False
    
    return True

# おこうとしている位置のどこかのブロックの下にちゃんと既存のブロックがあって，おくことができる場所であるかをチェックする
def CanPut(mainBoard:List[int], occupiedPositions:List[Tuple[int]]) -> bool:
    for pos in occupiedPositions:
        if pos[1] + 1 < BOARD_HEIGHT and mainBoard[pos[1]+1] & (0b1000000000 >> pos[0]) > 0:
            return True
        elif pos[1] + 1 == BOARD_HEIGHT:
            return True
    return False
