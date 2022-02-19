from enum import Enum, auto
from lib.constants.move import MOVE

class DIRECTION(Enum):
    N = auto()
    S = auto()
    W = auto()
    E = auto()

# 方角と回転を受け取って，回転したあとの方角を出力する
def GetNewDirection(direction, move):
    if direction is DIRECTION.N:
        if move is MOVE.L_ROT:
            return DIRECTION.W
        else:
            return DIRECTION.E
    elif direction is DIRECTION.E:
        if move is MOVE.L_ROT:
            return DIRECTION.N
        else:
            return DIRECTION.S
    elif direction is DIRECTION.S:
        if move is MOVE.L_ROT:
            return DIRECTION.E
        else:
            return DIRECTION.W
    else:
        if move is MOVE.L_ROT:
            return DIRECTION.S
        else:
            return DIRECTION.N