from constants.position import BOARD_HEIGHT, WINDOW_X, WINDOW_Y, WINDOW_HEIGHT, WINDOW_WIDTH
from constants.board import Board
from helpers.print import PrintBoardWithColor
from helpers.timer import Timer
from helpers.input import PressEnter
import mss
import mss.tools
from PIL import Image
import time
import boardWatcher
from init import Init

# ゲーム画面を認識して標準出力に出力する関数（無限ループ）
def PytrisBoardWatcher ():
    print("\n\nPy-tris Board Watcher\n\n")

    # ゲームの再開
    PressEnter()
    time.sleep(0.5)

    # 盤面を出力する分の行数を確保する
    for _ in range(BOARD_HEIGHT):
        print("", flush=True)
    
    # boardオブジェクトの生成
    board = Board()

    # メインループ
    while True:
        with mss.mss() as sct:
            a = Timer()
            # キャプチャする範囲は1P側の半分で十分
            region = {'top': WINDOW_Y, 'left': WINDOW_X, 'width': WINDOW_WIDTH / 2, 'height': WINDOW_HEIGHT}
            img = sct.grab(region)
            img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
            board.mainBoard = boardWatcher.GetMainBoardWithColor(img)
            board.followingMinos = boardWatcher.GetFollowingMinos(img)
            board.holdMino = boardWatcher.GetHoldMino(img)
            PrintBoardWithColor(board, True, a.Stop())


if __name__ == "__main__":
    # ゲームの初期設定
    Init()
    
    PytrisBoardWatcher()
    
