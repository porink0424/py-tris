from lib.constants import *
from lib.warning import *

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

# 受け取ったdirectedMinoが占領する場所に関するstringを返す
def EncodePlacesOccupiedByDirectedMino (directedMino:DirectedMino) -> str:
    occupiedPositions = sorted(GetOccupiedPositions(directedMino))
    ret = ""
    for i,j in occupiedPositions:
        ret += str(i) + "," + str(j) + ","
    return ret

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
        else:
            Error("Invalid kind of direction of directedMino.")
    
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
        else:
            Error("Invalid kind of direction of directedMino.")
    
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
        else:
            Error("Invalid kind of direction of directedMino.")
    
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
        else:
            Error("Invalid kind of direction of directedMino.")
    
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
        else:
            Error("Invalid kind of direction of directedMino.")
    
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
        else:
            Error("Invalid kind of direction of directedMino.")

    else:
        Error("Invalid kind of directedMino.")