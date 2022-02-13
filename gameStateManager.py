from constants.position import BOARD_HEIGHT
from helpers.print import PrintBoardWithColor
from helpers.timer import Timer
import pyautogui
import mss
import mss.tools
from PIL import Image
import time
import os
import boardWatcher


# ポーズメニューからプレイ画面に復帰
def Resume():
    pyautogui.press("Enter")



if __name__ == "__main__":
    # windowサイズを固定する
    os.system(
        "osascript -e 'tell application \"Parallels Desktop\"' -e 'set bounds of front window to {0,0,1795,1100}' -e 'end tell'"
    )

    # windowをアクティブにする
    pyautogui.click(100,100)
    time.sleep(0.5)

    # ゲームの再開
    # Resume()
    time.sleep(0.5)

    
    for _ in range(BOARD_HEIGHT):
        print("", flush=True)

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

    