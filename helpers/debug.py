import pyautogui
import time

# デバッグ用：何かしらのpositionのデータを取りたいときに回すループ
def DebugPosition():
    while True:
        print(pyautogui.position())
        time.sleep(1)