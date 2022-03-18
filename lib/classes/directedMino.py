from lib.constants import *

# 1つのミノの情報を，方角と中心位置で持つクラス
# 注意：Iミノは4×4の格子上に中心があるので，そのすぐ左上の点を中心の点としてみなしてデータを持つことにする
class DirectedMino ():
    def __init__(self, mino:MinoInt, direction:DirectionInt, pos:Tuple[int]):
        self.mino = mino
        self.direction = direction
        self.pos = pos

# 0 <= x < Aのとき
# (x, y) <-> y * A + x
# の1対1の対応関係を考えてEncodeする。
def EncodeDirectedMino (directedMino:DirectedMino) -> int:
    assert 0 <= directedMino.mino < 9
    assert 0 <= directedMino.direction < 4
    assert 0 <= directedMino.pos[0] + 1 < BOARD_WIDTH + 2
    assert 0 <= directedMino.pos[1] + 1 < BOARD_HEIGHT + 2
    return ((directedMino.mino * 4 + directedMino.direction) * (BOARD_WIDTH + 2) + directedMino.pos[0] + 1) * (BOARD_HEIGHT + 2) + directedMino.pos[1] + 1

# Encodeの方法に基づいてDecode
def DecodeDirectedMino (encodedDirectedMino:int) -> DirectedMino:

    encodedDirectedMino, pos1 = divmod(encodedDirectedMino, BOARD_HEIGHT + 2)
    encodedDirectedMino, pos0 = divmod(encodedDirectedMino, BOARD_WIDTH + 2)
    mino, direction = divmod(encodedDirectedMino, 4)
    pos1 -= 1
    pos0 -= 1

    return DirectedMino(
        mino,
        direction,
        (int(pos0), int(pos1))
    )

# 受け取ったdirectedMinoが占領する場所を示す数値を返す
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
# この関数の返り値を変更すると初期化の配列自体が変更されるため、返り値を変更したい場合はcopyすること。
def GetOccupiedPositions (directedMino:DirectedMino) -> List[Tuple[int]]:
    assert 0 <= directedMino.mino < 7
    assert 0 <= directedMino.direction < 4
    assert 0 <= directedMino.pos[0] + 2 < BOARD_WIDTH + 4
    assert 0 <= directedMino.pos[1] + 2 < BOARD_HEIGHT + 4
    pos0, pos1 = directedMino.pos
    res = globaloccupiedPositions[directedMino.mino][directedMino.direction][pos0 + 2][pos1 + 2]
    return res


# よく使われる関数GetOccupiedPositionsを高速化するために前計算しておく。
# occupiedPositions[7][4][BOARD_WIDTH + 4][BOARD_HEIGHT + 4] 
# MINOは T, S, Z, L, J, O, Iがそれぞれ0, 1, 2, 3, 4, 5, 6であることを仮定して、それ以外の入力はassertで除外している。
# DIRECTIONも同様
# -2 <= pos0 < BOARD_WIDTH + 2, -2 <= pos1 < BOARD_HEIGHT + 2 を仮定
globaloccupiedPositions = []
def InitGetOccupiedPositions ():
    global globaloccupiedPositions
    globaloccupiedPositions = [[[[[] for _ in range(BOARD_HEIGHT + 4)] 
                                     for _ in range(BOARD_WIDTH + 4)] 
                                     for _ in range(4)] 
                                     for _ in range(7)]
   
    for pos0 in range(-2, BOARD_WIDTH + 2):
        for pos1 in range(-2, BOARD_HEIGHT + 2):
            # MINO.T
            globaloccupiedPositions[MINO.T][DIRECTION.N][pos0 + 2][pos1 + 2] = [(pos0-1, pos1), (pos0, pos1-1), (pos0, pos1), (pos0+1, pos1)]
            globaloccupiedPositions[MINO.T][DIRECTION.E][pos0 + 2][pos1 + 2] = [(pos0, pos1-1), (pos0, pos1), (pos0, pos1+1), (pos0+1, pos1)]
            globaloccupiedPositions[MINO.T][DIRECTION.S][pos0 + 2][pos1 + 2] = [(pos0-1, pos1), (pos0, pos1), (pos0, pos1+1), (pos0+1, pos1)]
            globaloccupiedPositions[MINO.T][DIRECTION.W][pos0 + 2][pos1 + 2] = [(pos0-1, pos1), (pos0, pos1-1), (pos0, pos1), (pos0, pos1+1)]
            # MINO.S
            globaloccupiedPositions[MINO.S][DIRECTION.N][pos0 + 2][pos1 + 2] = [(pos0-1, pos1), (pos0, pos1-1), (pos0, pos1), (pos0+1, pos1-1)]
            globaloccupiedPositions[MINO.S][DIRECTION.E][pos0 + 2][pos1 + 2] = [(pos0, pos1-1), (pos0, pos1), (pos0+1, pos1), (pos0+1, pos1+1)]
            globaloccupiedPositions[MINO.S][DIRECTION.S][pos0 + 2][pos1 + 2] = [(pos0-1, pos1+1), (pos0, pos1), (pos0, pos1+1), (pos0+1, pos1)]
            globaloccupiedPositions[MINO.S][DIRECTION.W][pos0 + 2][pos1 + 2] = [(pos0-1, pos1-1), (pos0-1, pos1), (pos0, pos1), (pos0, pos1+1)]
            # MINO.Z
            globaloccupiedPositions[MINO.Z][DIRECTION.N][pos0 + 2][pos1 + 2] = [(pos0-1, pos1-1), (pos0, pos1-1), (pos0, pos1), (pos0+1, pos1)]
            globaloccupiedPositions[MINO.Z][DIRECTION.E][pos0 + 2][pos1 + 2] = [(pos0, pos1), (pos0, pos1+1), (pos0+1, pos1-1), (pos0+1, pos1)]
            globaloccupiedPositions[MINO.Z][DIRECTION.S][pos0 + 2][pos1 + 2] = [(pos0-1, pos1), (pos0, pos1), (pos0, pos1+1), (pos0+1, pos1+1)]
            globaloccupiedPositions[MINO.Z][DIRECTION.W][pos0 + 2][pos1 + 2] = [(pos0-1, pos1), (pos0-1, pos1+1), (pos0, pos1-1), (pos0, pos1)]
            # MINO.L
            globaloccupiedPositions[MINO.L][DIRECTION.N][pos0 + 2][pos1 + 2] = [(pos0-1, pos1), (pos0, pos1), (pos0+1, pos1-1), (pos0+1, pos1)]
            globaloccupiedPositions[MINO.L][DIRECTION.E][pos0 + 2][pos1 + 2] = [(pos0, pos1-1), (pos0, pos1), (pos0, pos1+1), (pos0+1, pos1+1)]
            globaloccupiedPositions[MINO.L][DIRECTION.S][pos0 + 2][pos1 + 2] = [(pos0-1, pos1), (pos0-1, pos1+1), (pos0, pos1), (pos0+1, pos1)]
            globaloccupiedPositions[MINO.L][DIRECTION.W][pos0 + 2][pos1 + 2] = [(pos0-1, pos1-1), (pos0, pos1-1), (pos0, pos1), (pos0, pos1+1)]
            # MINO.J
            globaloccupiedPositions[MINO.J][DIRECTION.N][pos0 + 2][pos1 + 2] = [(pos0-1, pos1-1), (pos0-1, pos1), (pos0, pos1), (pos0+1, pos1)]
            globaloccupiedPositions[MINO.J][DIRECTION.E][pos0 + 2][pos1 + 2] = [(pos0, pos1-1), (pos0, pos1), (pos0, pos1+1), (pos0+1, pos1-1)]
            globaloccupiedPositions[MINO.J][DIRECTION.S][pos0 + 2][pos1 + 2] = [(pos0-1, pos1), (pos0, pos1), (pos0+1, pos1), (pos0+1, pos1+1)]
            globaloccupiedPositions[MINO.J][DIRECTION.W][pos0 + 2][pos1 + 2] = [(pos0-1, pos1+1), (pos0, pos1-1), (pos0, pos1), (pos0, pos1+1)]
            # MINO.O
            globaloccupiedPositions[MINO.O][DIRECTION.N][pos0 + 2][pos1 + 2] = [(pos0, pos1-1), (pos0, pos1), (pos0+1, pos1-1), (pos0+1, pos1)]
            globaloccupiedPositions[MINO.O][DIRECTION.E][pos0 + 2][pos1 + 2] = [(pos0, pos1-1), (pos0, pos1), (pos0+1, pos1-1), (pos0+1, pos1)]
            globaloccupiedPositions[MINO.O][DIRECTION.S][pos0 + 2][pos1 + 2] = [(pos0, pos1-1), (pos0, pos1), (pos0+1, pos1-1), (pos0+1, pos1)]
            globaloccupiedPositions[MINO.O][DIRECTION.W][pos0 + 2][pos1 + 2] = [(pos0, pos1-1), (pos0, pos1), (pos0+1, pos1-1), (pos0+1, pos1)]
            # MINO.I
            globaloccupiedPositions[MINO.I][DIRECTION.N][pos0 + 2][pos1 + 2] = [(pos0-1, pos1), (pos0, pos1), (pos0+1, pos1), (pos0+2, pos1)]
            globaloccupiedPositions[MINO.I][DIRECTION.E][pos0 + 2][pos1 + 2] = [(pos0+1, pos1-1), (pos0+1, pos1), (pos0+1, pos1+1), (pos0+1, pos1+2)]
            globaloccupiedPositions[MINO.I][DIRECTION.S][pos0 + 2][pos1 + 2] = [(pos0-1, pos1+1), (pos0, pos1+1), (pos0+1, pos1+1), (pos0+2, pos1+1)]
            globaloccupiedPositions[MINO.I][DIRECTION.W][pos0 + 2][pos1 + 2] = [(pos0, pos1-1), (pos0, pos1), (pos0, pos1+1), (pos0, pos1+2)]
