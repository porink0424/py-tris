from enum import Enum, auto
from lib.constants.move import MOVE
from lib.warning import *

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
        elif move is MOVE.R_ROT:
            return DIRECTION.E
        else:
            Error("Invalid kind of moves.")
    elif direction is DIRECTION.E:
        if move is MOVE.L_ROT:
            return DIRECTION.N
        elif move is MOVE.R_ROT:
            return DIRECTION.S
        else:
            Error("Invalid kind of moves.")
    elif direction is DIRECTION.S:
        if move is MOVE.L_ROT:
            return DIRECTION.E
        elif move is MOVE.R_ROT:
            return DIRECTION.W
        else:
            Error("Invalid kind of moves.")
    else:
        if move is MOVE.L_ROT:
            return DIRECTION.S
        elif move is MOVE.R_ROT:
            return DIRECTION.N
        else:
            Error("Invalid kind of moves.")