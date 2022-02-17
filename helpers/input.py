import pyautogui
import time
from constants.move import MOVE

KEY_HOLD_TIME = 0.05

def Move (move:MOVE):
    if move is MOVE.LEFT:
        pyautogui.keyDown("left")
        time.sleep(KEY_HOLD_TIME) # 一定時間keyDownしていないと，認識されないことがある
        pyautogui.keyUp("left")
    elif move is MOVE.RIGHT:
        pyautogui.keyDown("right")
        time.sleep(KEY_HOLD_TIME)
        pyautogui.keyUp("right")
    elif move is MOVE.DOWN:
        pyautogui.keyDown("down")
        time.sleep(KEY_HOLD_TIME)
        pyautogui.keyUp("down")
    elif move is MOVE.DROP:
        pyautogui.keyDown("space")
        time.sleep(KEY_HOLD_TIME)
        pyautogui.keyUp("space")
    elif move is MOVE.HOLD:
        pyautogui.keyDown("c")
        time.sleep(KEY_HOLD_TIME)
        pyautogui.keyUp("c")
    elif move is MOVE.R_ROT:
        pyautogui.keyDown("x")
        time.sleep(KEY_HOLD_TIME)
        pyautogui.keyUp("x")
    elif move is MOVE.L_ROT:
        pyautogui.keyDown("z")
        time.sleep(KEY_HOLD_TIME)
        pyautogui.keyUp("z")

def PressEnter ():
    pyautogui.keyDown("Enter")
    time.sleep(KEY_HOLD_TIME)
    pyautogui.keyUp("Enter")