from enum import Enum, auto

class MOVE(Enum):
    LEFT = auto()
    RIGHT = auto()
    DOWN = auto()
    DROP = auto()
    HOLD = auto()
    R_ROT = auto()
    L_ROT = auto()

# 盤面中心で左右に線対称なミノ移動を返す
def ReflectMove(move:MOVE) -> MOVE:
    if move is MOVE.LEFT:
        return MOVE.RIGHT
    elif move is MOVE.RIGHT:
        return MOVE.LEFT
    elif move is MOVE.R_ROT:
        return MOVE.L_ROT
    elif move is MOVE.L_ROT:
        return MOVE.R_ROT
    else:
        return move

def ReflectMoves(moves:List[MOVE]) -> List[MOVE]:
    return [ReflectMove(move) for move in moves]