from lib.classes import *

try:
    import vgamepad as vg
    gamepad = vg.VX360Gamepad()
    print("Waiting for vgamepad connected...", flush=True)

    # gamepadの起動を待つ
    time.sleep(5)

    print("Done.", flush=True)
except:
    pass

KEY_HOLD_TIME = 0.02
KEY_RELEASE_TIME = 0.02

def Move (move:MOVE):
    if move is MOVE.LEFT:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
        gamepad.update()
        time.sleep(KEY_HOLD_TIME)
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
    elif move is MOVE.RIGHT:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
        gamepad.update()
        time.sleep(KEY_HOLD_TIME)
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
    elif move is MOVE.DOWN:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
        gamepad.update()
        time.sleep(KEY_HOLD_TIME)
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
    elif move is MOVE.DROP:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        gamepad.update()
        time.sleep(KEY_HOLD_TIME)
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
    elif move is MOVE.HOLD:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        gamepad.update()
        time.sleep(KEY_HOLD_TIME)
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    elif move is MOVE.R_ROT:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        gamepad.update()
        time.sleep(KEY_HOLD_TIME)
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    elif move is MOVE.L_ROT:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        gamepad.update()
        time.sleep(KEY_HOLD_TIME)
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()
    time.sleep(KEY_RELEASE_TIME)

def HoldDown ():
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
    gamepad.update()

def ReleaseDown ():
    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
    gamepad.update()

def PressEnter ():
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()
    time.sleep(KEY_HOLD_TIME)
    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()
    time.sleep(KEY_RELEASE_TIME)
