from lib.classes import *
from lib.helpers.check import isValidPlace

# moveの方向にdirectedMinoを回転しようとしたとき，directedMinoが回転成功するならば実行後のdirectedMinoを，回転失敗するならばNoneを返す
def Rotate (directedMino:DirectedMino, move:MoveInt, mainBoard:List[int]) -> Union[None, DirectedMino]:
    """
    以下，Tetris Design GuidelineにおけるSRSの内容を要約したものである。

    テトリスにおける回転入れは，Iミノ以外の場合，以下の流れがとられる（SRSと呼ばれる）:

    1. 中心位置を変えずにそのままの場所で回転する
    2. 中心位置を左右に動かす
    3. その状態から中心位置を上下に動かす
    4. 元に戻し，中心位置を上下に2マス動かす
    5. その状態から中心位置を左右に動かす

    上の5種類全て失敗した場合のみ，回転入れが失敗となり，ミノはその場にとどまる。なお，左右・上下のどちらに移動するかは初期状態・回転方向に依存する。

    Iミノの場合も同様だが，やや違いがある。詳しくはガイドラインを参照。
    """

    # Iミノの回転入れ
    if directedMino.mino is MINO.I:
        offsets = OFFSETS_I[directedMino.direction][move]
    # Iミノ以外のミノの回転入れ
    else:
        offsets = OFFSETS_EXCEPT_I[directedMino.direction][move]

    # SRSに従って上記の1~5を順番に実行する
    for offset0, offset1 in offsets:
        newDirectedMino = DirectedMino(
            directedMino.mino,
            GetNewDirection(directedMino.direction, move),
            (directedMino.pos[0] + offset0, directedMino.pos[1] + offset1)
        )
        occupiedPositons = GetOccupiedPositions(newDirectedMino)
        if isValidPlace(mainBoard, occupiedPositons):
            return newDirectedMino
    
    # どれも失敗してしまった場合
    return None

# 何番目の回転が成功したかを返す
# どの回転も成功しない場合Noneを返す
def GetRotateNum (directedMino:DirectedMino, move:MoveInt, mainBoard:List[int]) -> Union[None, int]:
    # Iミノの回転入れ
    if directedMino.mino is MINO.I:
        offsets = OFFSETS_I[directedMino.direction][move]
    # Iミノ以外のミノの回転入れ
    else:
        offsets = OFFSETS_EXCEPT_I[directedMino.direction][move]

    # SRSに従って上記の1~5を順番に実行する
    for i in range(len(offsets)):
        newDirectedMino = DirectedMino(
            directedMino.mino,
            GetNewDirection(directedMino.direction, move),
            (directedMino.pos[0] + offsets[i][0], directedMino.pos[1] + offsets[i][1])
        )
        occupiedPositons = GetOccupiedPositions(newDirectedMino)
        if isValidPlace(mainBoard, occupiedPositons):
            return i
    
    # どれも失敗してしまった場合
    return None