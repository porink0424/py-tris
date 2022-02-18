from enum import Enum, auto
from typing import Tuple, List
from constants.move import MOVE

class MINO(Enum):
    T = auto()
    O = auto()
    Z = auto()
    I = auto()
    L = auto()
    S = auto()
    J = auto()
    JAMA = auto()
    NONE = auto()

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

# 1つのミノの情報を，方角と中心位置で持つクラス
# 注意：Iミノは4×4の格子上に中心があるので，そのすぐ左上の点を中心の点としてみなしてデータを持つことにする
class DirectedMino ():
    def __init__(self, mino:MINO, direction:DIRECTION, pos:Tuple[int]):
        self.mino = mino
        self.direction = direction
        self.pos = pos

def EncodeDirectedMino (directedMino:DirectedMino) -> str:
    return f"{directedMino.mino},{directedMino.direction},{directedMino.pos[0]},{directedMino.pos[1]}"

def DecodeDirectedMino (encodedDirectedMino:str) -> DirectedMino:
    lis = encodedDirectedMino.split(",")
    return DirectedMino(
        eval(lis[0]),
        eval(lis[1]),
        (int(lis[2]), int(lis[3]))
    )

# directedMinoを受け取り，そのミノが占領するmainBoard上の位置を返す
def GetOccupiedPositions (directedMino:DirectedMino) -> List[Tuple[int]]:
    if directedMino.mino is MINO.T:
        if directedMino.direction is DIRECTION.N:
            pos = directedMino.pos
            return [pos, (pos[0]-1, pos[1]), (pos[0]+1, pos[1]), (pos[0], pos[1]-1)]
        elif directedMino.direction is DIRECTION.E:
            pos = directedMino.pos
            return [pos, (pos[0], pos[1]+1), (pos[0]+1, pos[1]), (pos[0], pos[1]-1)]
        elif directedMino.direction is DIRECTION.S:
            pos = directedMino.pos
            return [pos, (pos[0], pos[1]+1), (pos[0]+1, pos[1]), (pos[0]-1, pos[1])]
        elif directedMino.direction is DIRECTION.W:
            pos = directedMino.pos
            return [pos, (pos[0], pos[1]+1), (pos[0], pos[1]-1), (pos[0]-1, pos[1])]
    
    elif directedMino.mino is MINO.S:
        if directedMino.direction is DIRECTION.N:
            pos = directedMino.pos
            return [pos, (pos[0], pos[1]-1), (pos[0]+1, pos[1]-1), (pos[0]-1, pos[1])]
        elif directedMino.direction is DIRECTION.E:
            pos = directedMino.pos
            return [pos, (pos[0]+1, pos[1]), (pos[0]+1, pos[1]+1), (pos[0], pos[1]-1)]
        elif directedMino.direction is DIRECTION.S:
            pos = directedMino.pos
            return [pos, (pos[0]+1, pos[1]), (pos[0], pos[1]+1), (pos[0]-1, pos[1]+1)]
        elif directedMino.direction is DIRECTION.W:
            pos = directedMino.pos
            return [pos, (pos[0], pos[1]+1), (pos[0]-1, pos[1]), (pos[0]-1, pos[1]-1)]
    
    elif directedMino.mino is MINO.Z:
        if directedMino.direction is DIRECTION.N:
            pos = directedMino.pos
            return [pos, (pos[0], pos[1]-1), (pos[0]-1, pos[1]-1), (pos[0]+1, pos[1])]
        elif directedMino.direction is DIRECTION.E:
            pos = directedMino.pos
            return [pos, (pos[0]+1, pos[1]-1), (pos[0]+1, pos[1]), (pos[0], pos[1]+1)]
        elif directedMino.direction is DIRECTION.S:
            pos = directedMino.pos
            return [pos, (pos[0]-1, pos[1]), (pos[0], pos[1]+1), (pos[0]+1, pos[1]+1)]
        elif directedMino.direction is DIRECTION.W:
            pos = directedMino.pos
            return [pos, (pos[0], pos[1]-1), (pos[0]-1, pos[1]), (pos[0]-1, pos[1]+1)]
    
    elif directedMino.mino is MINO.L:
        if directedMino.direction is DIRECTION.N:
            pos = directedMino.pos
            return [pos, (pos[0]-1, pos[1]), (pos[0]+1, pos[1]), (pos[0]+1, pos[1]-1)]
        elif directedMino.direction is DIRECTION.E:
            pos = directedMino.pos
            return [pos, (pos[0], pos[1]-1), (pos[0], pos[1]+1), (pos[0]+1, pos[1]+1)]
        elif directedMino.direction is DIRECTION.S:
            pos = directedMino.pos
            return [pos, (pos[0]-1, pos[1]), (pos[0]-1, pos[1]+1), (pos[0]+1, pos[1])]
        elif directedMino.direction is DIRECTION.W:
            pos = directedMino.pos
            return [pos, (pos[0]-1, pos[1]-1), (pos[0], pos[1]-1), (pos[0], pos[1]+1)]
    
    elif directedMino.mino is MINO.J:
        if directedMino.direction is DIRECTION.N:
            pos = directedMino.pos
            return [pos, (pos[0]-1, pos[1]-1), (pos[0]-1, pos[1]), (pos[0]+1, pos[1])]
        elif directedMino.direction is DIRECTION.E:
            pos = directedMino.pos
            return [pos, (pos[0], pos[1]-1), (pos[0]+1, pos[1]-1), (pos[0], pos[1]+1)]
        elif directedMino.direction is DIRECTION.S:
            pos = directedMino.pos
            return [pos, (pos[0]-1, pos[1]), (pos[0]+1, pos[1]), (pos[0]+1, pos[1]+1)]
        elif directedMino.direction is DIRECTION.W:
            pos = directedMino.pos
            return [pos, (pos[0], pos[1]-1), (pos[0]-1, pos[1]+1), (pos[0], pos[1]+1)]
    
    elif directedMino.mino is MINO.O:
        pos = directedMino.pos
        return [pos, (pos[0], pos[1]-1), (pos[0]+1, pos[1]), (pos[0]+1, pos[1]-1)]

    elif directedMino.mino is MINO.I:
        if directedMino.direction is DIRECTION.N:
            pos = directedMino.pos
            return [pos, (pos[0]-1, pos[1]), (pos[0]+1, pos[1]), (pos[0]+2, pos[1])]
        elif directedMino.direction is DIRECTION.E:
            pos = directedMino.pos
            return [(pos[0]+1, pos[1]-1), (pos[0]+1, pos[1]), (pos[0]+1, pos[1]+1), (pos[0]+1, pos[1]+2)]
        elif directedMino.direction is DIRECTION.S:
            pos = directedMino.pos
            return [(pos[0]-1, pos[1]+1), (pos[0], pos[1]+1), (pos[0]+1, pos[1]+1), (pos[0]+2, pos[1]+1)]
        elif directedMino.direction is DIRECTION.W:
            pos = directedMino.pos
            return [pos, (pos[0], pos[1]-1), (pos[0], pos[1]+1), (pos[0], pos[1]+2)]
