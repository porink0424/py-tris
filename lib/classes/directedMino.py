from lib.constants import *

# 1つのミノの情報を，方角と中心位置で持つクラス
# 注意：Iミノは4×4の格子上に中心があるので，そのすぐ左上の点を中心の点としてみなしてデータを持つことにする
class DirectedMino ():
    def __init__(self, mino:MINO, direction:DIRECTION, pos:Tuple[int]):
        self.mino = mino
        self.direction = direction
        self.pos = pos

def EncodeDirectedMino (directedMino:DirectedMino) -> int:
    assert 0 <= directedMino.mino.value < 9
    assert 0 <= directedMino.direction.value < 4
    assert 0 <= directedMino.pos[0] + 1 < BOARD_WIDTH + 2
    assert 0 <= directedMino.pos[1] + 1 < BOARD_HEIGHT + 2
    return ((directedMino.mino.value * 4 + directedMino.direction.value) * (BOARD_WIDTH + 2) + directedMino.pos[0] + 1) * (BOARD_HEIGHT + 2) + directedMino.pos[1] + 1

def DecodeDirectedMino (encodedDirectedMino:int) -> DirectedMino:

    (encodedDirectedMino, pos1) = divmod(encodedDirectedMino, BOARD_HEIGHT + 2)
    (encodedDirectedMino, pos0) = divmod(encodedDirectedMino, BOARD_WIDTH + 2)
    (mino, direction) = divmod(encodedDirectedMino, 4)
    pos1 -= 1
    pos0 -= 1

    return DirectedMino(
        MINO(mino),
        DIRECTION(direction),
        (int(pos0), int(pos1))
    )

# 受け取ったdirectedMinoが占領する場所に関するstringを返す
def EncodePlacesOccupiedByDirectedMino (directedMino:DirectedMino) -> int:
    occupiedPositions = GetOccupiedPositions(directedMino)
    ret = 0
    maxPos = BOARD_WIDTH * BOARD_HEIGHT
    for i,j in occupiedPositions:
        assert 0 <= i < BOARD_WIDTH
        assert 0 <= j < BOARD_HEIGHT
        ret = ret * maxPos + i * BOARD_HEIGHT + j
    return ret

# directedMinoを受け取り，そのミノが占領するmainBoard上の位置をsortして返す
def GetOccupiedPositions (directedMino:DirectedMino) -> List[Tuple[int]]:
    pos0, pos1 = directedMino.pos
    if directedMino.mino is MINO.T:
        if directedMino.direction is DIRECTION.N:
            return [(pos0-1, pos1), (pos0, pos1-1), (pos0, pos1), (pos0+1, pos1)]
        elif directedMino.direction is DIRECTION.E:
            return [(pos0, pos1-1), (pos0, pos1), (pos0, pos1+1), (pos0+1, pos1)]
        elif directedMino.direction is DIRECTION.S:
            return [(pos0-1, pos1), (pos0, pos1), (pos0, pos1+1), (pos0+1, pos1)]
        elif directedMino.direction is DIRECTION.W:
            return [(pos0-1, pos1), (pos0, pos1-1), (pos0, pos1), (pos0, pos1+1)]
    
    elif directedMino.mino is MINO.S:
        if directedMino.direction is DIRECTION.N:
            return [(pos0-1, pos1), (pos0, pos1-1), (pos0, pos1), (pos0+1, pos1-1)]
        elif directedMino.direction is DIRECTION.E:
            return [(pos0, pos1-1), (pos0, pos1), (pos0+1, pos1), (pos0+1, pos1+1)]
        elif directedMino.direction is DIRECTION.S:
            return [(pos0-1, pos1+1), (pos0, pos1), (pos0, pos1+1), (pos0+1, pos1)]
        elif directedMino.direction is DIRECTION.W:
            return [(pos0-1, pos1-1), (pos0-1, pos1), (pos0, pos1), (pos0, pos1+1)]
    
    elif directedMino.mino is MINO.Z:
        if directedMino.direction is DIRECTION.N:
            return [(pos0-1, pos1-1), (pos0, pos1-1), (pos0, pos1), (pos0+1, pos1)]
        elif directedMino.direction is DIRECTION.E:
            return [(pos0, pos1), (pos0, pos1+1), (pos0+1, pos1-1), (pos0+1, pos1)]
        elif directedMino.direction is DIRECTION.S:
            return [(pos0-1, pos1), (pos0, pos1), (pos0, pos1+1), (pos0+1, pos1+1)]
        elif directedMino.direction is DIRECTION.W:
            return [(pos0-1, pos1), (pos0-1, pos1+1), (pos0, pos1-1), (pos0, pos1)]
    
    elif directedMino.mino is MINO.L:
        if directedMino.direction is DIRECTION.N:
            return [(pos0-1, pos1), (pos0, pos1), (pos0+1, pos1-1), (pos0+1, pos1)]
        elif directedMino.direction is DIRECTION.E:
            return [(pos0, pos1-1), (pos0, pos1), (pos0, pos1+1), (pos0+1, pos1+1)]
        elif directedMino.direction is DIRECTION.S:
            return [(pos0-1, pos1), (pos0-1, pos1+1), (pos0, pos1), (pos0+1, pos1)]
        elif directedMino.direction is DIRECTION.W:
            return [(pos0-1, pos1-1), (pos0, pos1-1), (pos0, pos1), (pos0, pos1+1)]
    
    elif directedMino.mino is MINO.J:
        if directedMino.direction is DIRECTION.N:
            return [(pos0-1, pos1-1), (pos0-1, pos1), (pos0, pos1), (pos0+1, pos1)]
        elif directedMino.direction is DIRECTION.E:
            return [(pos0, pos1-1), (pos0, pos1), (pos0, pos1+1), (pos0+1, pos1-1)]
        elif directedMino.direction is DIRECTION.S:
            return [(pos0-1, pos1), (pos0, pos1), (pos0+1, pos1), (pos0+1, pos1+1)]
        elif directedMino.direction is DIRECTION.W:
            return [(pos0-1, pos1+1), (pos0, pos1-1), (pos0, pos1), (pos0, pos1+1)]
    
    elif directedMino.mino is MINO.O:
        return [(pos0, pos1-1), (pos0, pos1), (pos0+1, pos1-1), (pos0+1, pos1)]

    elif directedMino.mino is MINO.I:
        if directedMino.direction is DIRECTION.N:
            return [(pos0-1, pos1), (pos0, pos1), (pos0+1, pos1), (pos0+2, pos1)]
        elif directedMino.direction is DIRECTION.E:
            return [(pos0+1, pos1-1), (pos0+1, pos1), (pos0+1, pos1+1), (pos0+1, pos1+2)]
        elif directedMino.direction is DIRECTION.S:
            return [(pos0-1, pos1+1), (pos0, pos1+1), (pos0+1, pos1+1), (pos0+2, pos1+1)]
        elif directedMino.direction is DIRECTION.W:
            return [(pos0, pos1-1), (pos0, pos1), (pos0, pos1+1), (pos0, pos1+2)]