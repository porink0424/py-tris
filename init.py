import pyautogui
import os
import time

def init():
    pyautogui.PAUSE = 0

    # windowサイズを固定する
    os.system(
        "osascript -e 'tell application \"Parallels Desktop\"' -e 'set bounds of front window to {0,0,1795,1100}' -e 'end tell'"
    )

    # windowをアクティブにする
    pyautogui.click(100,100)
    time.sleep(0.5)