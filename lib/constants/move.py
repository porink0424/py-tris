
# MOVEはクラス定数
# 型の検査がなくなるため高速化
class MOVE():
    LEFT = 0
    RIGHT = 1
    DOWN = 2
    DROP = 3
    HOLD = 4
    R_ROT = 5
    L_ROT = 6

# intのエイリアスとしてMoveIntを定義
MoveInt = int