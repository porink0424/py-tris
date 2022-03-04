from lib.constants import *

# 1つのミノの情報を，方角と中心位置で持つクラス
# 注意：Iミノは4×4の格子上に中心があるので，そのすぐ左上の点を中心の点としてみなしてデータを持つことにする
class DirectedMino ():
    def __init__(self, mino:MINO, direction:DIRECTION, pos:Tuple[int]):
        self.mino = mino
        self.direction = direction
        self.pos = pos

# 0 <= x < Aのとき
# (x, y) <-> y * A + x
# の1対1の対応関係を考えてEncodeする。
def EncodeDirectedMino (directedMino:DirectedMino) -> int:
    assert 0 <= directedMino.mino.value < 9
    assert 0 <= directedMino.direction.value < 4
    assert 0 <= directedMino.pos[0] + 1 < BOARD_WIDTH + 2
    assert 0 <= directedMino.pos[1] + 1 < BOARD_HEIGHT + 2
    return ((directedMino.mino.value * 4 + directedMino.direction.value) * (BOARD_WIDTH + 2) + directedMino.pos[0] + 1) * (BOARD_HEIGHT + 2) + directedMino.pos[1] + 1

# Encodeの方法に基づいてDecode
def DecodeDirectedMino (encodedDirectedMino:int) -> DirectedMino:

    encodedDirectedMino, pos1 = divmod(encodedDirectedMino, BOARD_HEIGHT + 2)
    encodedDirectedMino, pos0 = divmod(encodedDirectedMino, BOARD_WIDTH + 2)
    mino, direction = divmod(encodedDirectedMino, 4)
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
    assert 0 <= directedMino.mino.value < 7
    assert 0 <= directedMino.direction.value < 4
    assert 0 <= directedMino.pos[0] + 2 < BOARD_WIDTH + 4
    assert 0 <= directedMino.pos[1] + 2 < BOARD_HEIGHT + 4
    pos0, pos1 = directedMino.pos
    return occupiedPositions[directedMino.mino.value][directedMino.direction.value][pos0 + 2][pos1 + 2]


# よく使われる関数GetOccupiedPositionsを高速化するために前計算しておく。
# occupiedPositions[7][4][BOARD_WIDTH + 4][BOARD_HEIGHT + 4] 
# MINOは T, S, Z, L, J, O, Iがそれぞれ0, 1, 2, 3, 4, 5, 6であることを仮定して、それ以外の入力はassertで除外している。
# DIRECTIONも同様
# -2 <= pos0 < BOARD_WIDTH + 2, -2 <= pos1 < BOARD_HEIGHT + 2 を仮定
occupiedPositions = []
def InitGetOccupiedPositions ():
    global occupiedPositions
    occupiedPositions = [[[[[] for _ in range(BOARD_HEIGHT + 4)] 
                               for _ in range(BOARD_WIDTH + 4)] 
                               for _ in range(4)] 
                               for _ in range(7)]
   
    for pos0 in range(-2, BOARD_WIDTH + 2):
        for pos1 in range(-2, BOARD_HEIGHT + 2):
            # MINO.T
            occupiedPositions[MINO.T.value][DIRECTION.N.value][pos0 + 2][pos1 + 2] = [(pos0-1, pos1), (pos0, pos1-1), (pos0, pos1), (pos0+1, pos1)]
            occupiedPositions[MINO.T.value][DIRECTION.E.value][pos0 + 2][pos1 + 2] = [(pos0, pos1-1), (pos0, pos1), (pos0, pos1+1), (pos0+1, pos1)]
            occupiedPositions[MINO.T.value][DIRECTION.S.value][pos0 + 2][pos1 + 2] = [(pos0-1, pos1), (pos0, pos1), (pos0, pos1+1), (pos0+1, pos1)]
            occupiedPositions[MINO.T.value][DIRECTION.W.value][pos0 + 2][pos1 + 2] = [(pos0-1, pos1), (pos0, pos1-1), (pos0, pos1), (pos0, pos1+1)]
            # MINO.S
            occupiedPositions[MINO.S.value][DIRECTION.N.value][pos0 + 2][pos1 + 2] = [(pos0-1, pos1), (pos0, pos1-1), (pos0, pos1), (pos0+1, pos1-1)]
            occupiedPositions[MINO.S.value][DIRECTION.E.value][pos0 + 2][pos1 + 2] = [(pos0, pos1-1), (pos0, pos1), (pos0+1, pos1), (pos0+1, pos1+1)]
            occupiedPositions[MINO.S.value][DIRECTION.S.value][pos0 + 2][pos1 + 2] = [(pos0-1, pos1+1), (pos0, pos1), (pos0, pos1+1), (pos0+1, pos1)]
            occupiedPositions[MINO.S.value][DIRECTION.W.value][pos0 + 2][pos1 + 2] = [(pos0-1, pos1-1), (pos0-1, pos1), (pos0, pos1), (pos0, pos1+1)]
            # MINO.Z
            occupiedPositions[MINO.Z.value][DIRECTION.N.value][pos0 + 2][pos1 + 2] = [(pos0-1, pos1-1), (pos0, pos1-1), (pos0, pos1), (pos0+1, pos1)]
            occupiedPositions[MINO.Z.value][DIRECTION.E.value][pos0 + 2][pos1 + 2] = [(pos0, pos1), (pos0, pos1+1), (pos0+1, pos1-1), (pos0+1, pos1)]
            occupiedPositions[MINO.Z.value][DIRECTION.S.value][pos0 + 2][pos1 + 2] = [(pos0-1, pos1), (pos0, pos1), (pos0, pos1+1), (pos0+1, pos1+1)]
            occupiedPositions[MINO.Z.value][DIRECTION.W.value][pos0 + 2][pos1 + 2] = [(pos0-1, pos1), (pos0-1, pos1+1), (pos0, pos1-1), (pos0, pos1)]
            # MINO.L
            occupiedPositions[MINO.L.value][DIRECTION.N.value][pos0 + 2][pos1 + 2] = [(pos0-1, pos1), (pos0, pos1), (pos0+1, pos1-1), (pos0+1, pos1)]
            occupiedPositions[MINO.L.value][DIRECTION.E.value][pos0 + 2][pos1 + 2] = [(pos0, pos1-1), (pos0, pos1), (pos0, pos1+1), (pos0+1, pos1+1)]
            occupiedPositions[MINO.L.value][DIRECTION.S.value][pos0 + 2][pos1 + 2] = [(pos0-1, pos1), (pos0-1, pos1+1), (pos0, pos1), (pos0+1, pos1)]
            occupiedPositions[MINO.L.value][DIRECTION.W.value][pos0 + 2][pos1 + 2] = [(pos0-1, pos1-1), (pos0, pos1-1), (pos0, pos1), (pos0, pos1+1)]
            # MINO.J
            occupiedPositions[MINO.J.value][DIRECTION.N.value][pos0 + 2][pos1 + 2] = [(pos0-1, pos1-1), (pos0-1, pos1), (pos0, pos1), (pos0+1, pos1)]
            occupiedPositions[MINO.J.value][DIRECTION.E.value][pos0 + 2][pos1 + 2] = [(pos0, pos1-1), (pos0, pos1), (pos0, pos1+1), (pos0+1, pos1-1)]
            occupiedPositions[MINO.J.value][DIRECTION.S.value][pos0 + 2][pos1 + 2] = [(pos0-1, pos1), (pos0, pos1), (pos0+1, pos1), (pos0+1, pos1+1)]
            occupiedPositions[MINO.J.value][DIRECTION.W.value][pos0 + 2][pos1 + 2] = [(pos0-1, pos1+1), (pos0, pos1-1), (pos0, pos1), (pos0, pos1+1)]
            # MINO.O
            occupiedPositions[MINO.O.value][DIRECTION.N.value][pos0 + 2][pos1 + 2] = [(pos0, pos1-1), (pos0, pos1), (pos0+1, pos1-1), (pos0+1, pos1)]
            occupiedPositions[MINO.O.value][DIRECTION.E.value][pos0 + 2][pos1 + 2] = [(pos0, pos1-1), (pos0, pos1), (pos0+1, pos1-1), (pos0+1, pos1)]
            occupiedPositions[MINO.O.value][DIRECTION.S.value][pos0 + 2][pos1 + 2] = [(pos0, pos1-1), (pos0, pos1), (pos0+1, pos1-1), (pos0+1, pos1)]
            occupiedPositions[MINO.O.value][DIRECTION.W.value][pos0 + 2][pos1 + 2] = [(pos0, pos1-1), (pos0, pos1), (pos0+1, pos1-1), (pos0+1, pos1)]
            # MINO.I
            occupiedPositions[MINO.I.value][DIRECTION.N.value][pos0 + 2][pos1 + 2] = [(pos0-1, pos1), (pos0, pos1), (pos0+1, pos1), (pos0+2, pos1)]
            occupiedPositions[MINO.I.value][DIRECTION.E.value][pos0 + 2][pos1 + 2] = [(pos0+1, pos1-1), (pos0+1, pos1), (pos0+1, pos1+1), (pos0+1, pos1+2)]
            occupiedPositions[MINO.I.value][DIRECTION.S.value][pos0 + 2][pos1 + 2] = [(pos0-1, pos1+1), (pos0, pos1+1), (pos0+1, pos1+1), (pos0+2, pos1+1)]
            occupiedPositions[MINO.I.value][DIRECTION.W.value][pos0 + 2][pos1 + 2] = [(pos0, pos1-1), (pos0, pos1), (pos0, pos1+1), (pos0, pos1+2)]
