from typing import List

# MINOはクラス定数
# 型の検査がなくなるため高速化
class MINO():
    T = 0
    O = 1
    Z = 2
    I = 3
    L = 4
    S = 5
    J = 6
    JAMA = 7
    NONE = 8

# intのエイリアスとしてMinIntを定義
MinoInt = int

def ReturnFullBag() -> List[MINO]:
    return [MINO.T, MINO.O, MINO.Z, MINO.I, MINO.L, MINO.S, MINO.J]
