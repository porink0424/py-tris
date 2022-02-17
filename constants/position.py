import subprocess
from constants.name import TITLE

# windowサイズを取得
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

# 盤面の大きさ
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# windowの位置・サイズ
WINDOW_TITLE_BAR_HEIGHT = 38
GAME_SCREEN_HEIGHT = WINDOW_HEIGHT - WINDOW_TITLE_BAR_HEIGHT # TITLE_BARを除いた，ゲーム画面自体の高さ

# 盤面の左上・右下のますの中心位置
TOP_LEFT_X = int((309/1795) * WINDOW_WIDTH) + WINDOW_X
TOP_LEFT_Y = int((176/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT + WINDOW_Y
TOP_RIGHT_X = int((609/1795) * WINDOW_WIDTH) + WINDOW_X
TOP_RIGHT_Y = int((844/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT + WINDOW_Y

# 各マスの大きさ
recWidth = (TOP_RIGHT_X - TOP_LEFT_X) / (BOARD_WIDTH - 1)
recHeight = (TOP_RIGHT_Y - TOP_LEFT_Y) / (BOARD_HEIGHT - 1)

# NEXTミノ以降のミノが表示されている位置のx座標と、y座標の範囲
NEXT_MINOS_X = int((730/1795) * WINDOW_WIDTH) + WINDOW_X
NEXT_MINOS_Y_RANGES = [
    (int((192/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT + WINDOW_Y, int((241/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT + WINDOW_Y),
    (int((279/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT + WINDOW_Y, int((339/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT + WINDOW_Y),
    (int((373/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT + WINDOW_Y, int((433/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT + WINDOW_Y),
    (int((460/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT + WINDOW_Y, int((520/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT + WINDOW_Y),
    (int((568/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT + WINDOW_Y, int((628/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT + WINDOW_Y),
]
NEXT_MINOS_BOX_X = int((657/1795) * WINDOW_WIDTH) + WINDOW_X

# HOLDミノが表示されている位置のx座標と、y座標の範囲
HOLD_MINO_X = int((270/1795) * WINDOW_WIDTH) + WINDOW_X
HOLD_MINO_Y_RANGE = (int((204/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT + WINDOW_Y, int((267/1056) * GAME_SCREEN_HEIGHT) + WINDOW_TITLE_BAR_HEIGHT + WINDOW_Y)
HOLD_MINO_BOX_X = int((169/1795) * WINDOW_WIDTH) + WINDOW_X