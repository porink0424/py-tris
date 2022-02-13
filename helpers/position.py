from constants.position import TOP_LEFT_X, TOP_LEFT_Y, recWidth, recHeight

# 上からi番目、左からj番目(0-index)のボックスの中心の座標を返す
def GetCenterPosition(i, j):
    return (
        int(TOP_LEFT_X + recWidth * j),
        int(TOP_LEFT_Y + recHeight * i),
    )