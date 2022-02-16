from constants.position import WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT
import pyautogui
import os
import time

def Init():
    pyautogui.PAUSE = 0

    # windowサイズを固定する
    window = "{{{},{},{},{}}}".format(WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT)
    os.system(
        f"osascript -e 'tell application \"Parallels Desktop\"' -e 'set bounds of front window to {window}' -e 'end tell'"
    )

    # windowをアクティブにする
    pyautogui.click(100,100)
    time.sleep(0.5)