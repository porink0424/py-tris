# 盤面の大きさ
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# 盤面の左上・右下のますの中心位置
TOP_LEFT_X = 309
TOP_LEFT_Y = 240
TOP_RIGHT_X = 609
TOP_RIGHT_Y = 908

# 各マスの大きさ
recWidth = (TOP_RIGHT_X - TOP_LEFT_X) / (BOARD_WIDTH - 1)
recHeight = (TOP_RIGHT_Y - TOP_LEFT_Y) / (BOARD_HEIGHT - 1)

# NEXTミノ以降のミノが表示されている位置のx座標と、y座標の範囲
NEXT_MINOS_X = 712
NEXT_MINOS_Y_RANGES = [
    (256,305), (343,403), (437,497), (535,595), (632,692),
]
NEXT_MINOS_BOX_X = 657

# HOLDミノが表示されている位置のx座標と、y座標の範囲
HOLD_MINO_X = 270
HOLD_MINO_Y_RANGE = (268, 331)
HOLD_MINO_BOX_X = 169