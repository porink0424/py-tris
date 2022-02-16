from constants.position import BOARD_HEIGHT
from constants.move import MOVE
from helpers.print import PrintBoardWithColor
from helpers.timer import Timer
from helpers.input import PressEnter, Move
import mss
import mss.tools
from PIL import Image
import time
import boardWatcher
from init import Init


# ポーズメニューからプレイ画面に復帰
def Resume():
    PressEnter()


if __name__ == "__main__":
    Init()

    print("\n\nPy-tris Board Watcher\n\n")

    # ゲームの再開
    Resume()
    time.sleep(0.5)

    for _ in range(BOARD_HEIGHT):
        print("", flush=True)
    
    for _ in range(5):
        Move(MOVE.RIGHT)
        Move(MOVE.RIGHT)
        Move(MOVE.DROP)
        time.sleep(0.1)

    while True:
        with mss.mss() as sct:
            a = Timer()
            region = {'top': 0, 'left': 0, 'width': 1795, 'height': 1100}
            img = sct.grab(region)
            img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
            boardColor = boardWatcher.GetBoardWithColor(img)
            followingMinos = boardWatcher.GetFollowingMinos(img)
            holdMino = boardWatcher.GetHoldMino(img)
            PrintBoardWithColor(boardColor, followingMinos, holdMino, True, a.Stop())
