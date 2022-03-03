import initSettings
import boardWatcher
import decisionMaker
import minoMover
import simulator
from lib import *

# ゲーム画面を認識して標準出力に出力する関数（無限ループ）
def PytrisBoardWatcher ():
    print("\n\nPy-tris Board Watcher\n\n")

    # ゲームの再開
    PressEnter()

    # 盤面を出力する分の行数を確保する
    for _ in range(DISPLAYED_BOARD_HEIGHT):
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
            board.mainBoard = boardWatcher.GetMainBoard(img)
            board.followingMinos = boardWatcher.GetFollowingMinos(img)
            board.holdMino = boardWatcher.GetHoldMino(img)
            PrintBoard(board, True, a.Stop())

# simulator上で思考を再現する（無限ループ）
def PytrisSimulator ():
    print("\n\nPy-tris Simulator\n\n")

    # 適当に盤面を生成
    board = Board()

    # board.AddBlockToMainBoard((5 ,38))
    # board.AddBlockToMainBoard((5 ,37))
    # board.AddBlockToMainBoard((4 ,37))
    # board.AddBlockToMainBoard((1 ,37))
    # board.AddBlockToMainBoard((1 ,38))
    # for i in range(10):
    #     board.AddBlockToMainBoard((i ,39))

    board.followingMinos = [simulator.GenerateMino() for _ in range(FOLLOWING_MINOS_COUNT)]
    print("\n\n\n")
    PrintBoard(board)

    while True:
        addedMino = simulator.GenerateMino()
        board = simulator.AddFollowingMino(board, addedMino)

        # 思考ルーチン
        value, mino, path = decisionMaker.Decide(board)

        board = simulator.PutMino(path, board.currentMino, board)

        newMainBoard, clearedRowCount = simulator.ClearLinesOfBoard(board)
        board = Board(
            newMainBoard,
            None,
            board.followingMinos,
            board.holdMino,
            True
        )

# 実機上で思考を再現する（無限ループ、シングルスレッド）
# Start Overを押せる状態からはじめないとバグる
def PytrisMover ():
    # ゲームの再開
    PressEnter()
    time.sleep(4.5)

    # 盤面を出力する分の行数を確保する
    for _ in range(DISPLAYED_BOARD_HEIGHT):
        print("", flush=True)

    while True:
        # 盤面の状況を読み取る
        with mss.mss() as sct:
            region = {'top': WINDOW_Y, 'left': WINDOW_X, 'width': WINDOW_WIDTH / 2, 'height': WINDOW_HEIGHT}
            img = sct.grab(region)
            img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
        currentMino = boardWatcher.GetCurrentMino(img)
        mainBoard = boardWatcher.GetMainBoard(img)
        deletedMainBoard = DeleteDirectedMinoFromMainBoard(currentMino, mainBoard)
        board = Board(
            deletedMainBoard,
            DirectedMino(currentMino.mino, DIRECTION.N, FIRST_MINO_POS),
            boardWatcher.GetFollowingMinos(img),
            boardWatcher.GetHoldMino(img),
            True
        )

        # 思考ルーチン
        value, mino, path = decisionMaker.Decide(board)

        # 移動
        directedMino = minoMover.InputMove(path, board.currentMino, board.mainBoard)

        # ライン消去
        joinedMainBoard = JoinDirectedMinoToBoard(directedMino, board.mainBoard)
        newMainBoard, clearedRowCount = ClearLines(joinedMainBoard)

        # AIが見ているはずの盤面の状況
        nowAIsMainBoard = Board(
            newMainBoard,
            None,
            board.followingMinos,
            board.holdMino,
            board.canHold
        )
        PrintBoard(nowAIsMainBoard, True)

        # currentMinoが更新されるのを待つ
        while True:
            currentMino = boardWatcher.GetCurrentMino()
            if board.followingMinos[0] is currentMino.mino: # currentMinoが更新されたら次へ
                break
    
        # クリアしたライン数に応じて待ち時間を変える
        FRAME_DELTA_TIME = 0.015
        FRAME_COUNTS = [1, 30, 38, 38, 38]
        time.sleep(FRAME_DELTA_TIME * FRAME_COUNTS[clearedRowCount])



def main():
    # ゲームの初期設定
    initSettings.Init()
    
    # # 盤面監視モード
    # PytrisBoardWatcher()

    # # simulatorモード
    # PytrisSimulator()

    # 実機確認モード
    PytrisMover()
