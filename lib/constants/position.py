import subprocess
from lib.constants.name import TITLE
from lib.constants.direction import DIRECTION

# 盤面の大きさ
BOARD_WIDTH = 10
BOARD_HEIGHT = 40
DISPLAYED_BOARD_HEIGHT = 20 # 実際に「表示」されている盤面の高さ
FOLLOWING_MINOS_COUNT = 5

# ミノの出現時の向き・位置
FIRST_MINO_POS = (5,20)
FIRST_MINO_DIRECTION = DIRECTION.N

# windowサイズを取得
try:
    process = subprocess.Popen(
        f"osascript -e 'tell application \"{TITLE}\" to get the bounds of the front window'",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate()
    windowInfo = stdout    \
        .decode("utf-8")   \
        .replace("\n", "") \
        .split(",")

    WINDOW_X = int(windowInfo[0])
    WINDOW_Y = int(windowInfo[1])
    WINDOW_WIDTH = int(windowInfo[2]) - WINDOW_X
    WINDOW_HEIGHT = int(windowInfo[3]) - WINDOW_Y
except:
    pass
else:
    # windowの位置・サイズ
    WINDOW_TITLE_BAR_HEIGHT = 38
    GAME_SCREEN_HEIGHT = WINDOW_HEIGHT - WINDOW_TITLE_BAR_HEIGHT # TITLE_BARを除いた，ゲーム画面自体の高さ

    # 盤面の左上・右下のますの中心位置
    TOP_LEFT_X = int((309/1795) * WINDOW_WIDTH)
    TOP_LEFT_Y = int((176/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT
    TOP_RIGHT_X = int((609/1795) * WINDOW_WIDTH)
    TOP_RIGHT_Y = int((844/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT

    # 各マスの大きさ
    recWidth = (TOP_RIGHT_X - TOP_LEFT_X) / (BOARD_WIDTH - 1)
    recHeight = (TOP_RIGHT_Y - TOP_LEFT_Y) / (BOARD_HEIGHT - 1)

    # NEXTミノ以降のミノが表示されている位置のx座標と、y座標の範囲
    NEXT_MINOS_X = int((730/1795) * WINDOW_WIDTH)
    NEXT_MINOS_Y_RANGES = [
        (int((192/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT, int((241/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT),
        (int((279/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT, int((339/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT),
        (int((373/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT, int((433/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT),
        (int((460/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT, int((520/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT),
        (int((568/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT, int((628/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT),
    ]
    NEXT_MINOS_BOX_X = int((657/1795) * WINDOW_WIDTH)

    # HOLDミノが表示されている位置のx座標と、y座標の範囲
    HOLD_MINO_X = int((270/1795) * WINDOW_WIDTH)
    HOLD_MINO_Y_RANGE = (int((204/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT, int((267/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT)
    HOLD_MINO_BOX_X = int((169/1795) * WINDOW_WIDTH)