from lib import *

def Init():
    # pyautoguiの遅延を0にする
    pyautogui.PAUSE = 0
    # GetOccupiedPositionsの前計算
    InitGetOccupiedPositions()

    try:
        # windowをアクティブにする
        pyautogui.click(WINDOW_X + 1, WINDOW_Y + 1)
        time.sleep(0.5)
    except:
        pass

