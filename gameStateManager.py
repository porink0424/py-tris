# -------------
#
# Init Settings
#
# -------------

import pyautogui
import time

# pyautoguiの遅延を0にする
pyautogui.PAUSE = 0

# windowの位置
# todo: 環境によって初期位置を調整する
WINDOW_X = 100
WINDOW_Y = 100

# windowをアクティブにする
pyautogui.click(WINDOW_X, WINDOW_Y)
print("Window activated.", flush=True)

import boardWatcher
import decisionMaker
import minoMover
import simulator
import evaluator
from lib import *
from params.eval import *

# GetOccupiedPositionsの前計算
InitGetOccupiedPositions()

# -------------
#
# Init Settings End
#
# -------------

# ゲーム画面を認識して標準出力に出力する関数（無限ループ）
def PytrisBoardWatcher ():
    print("\n\nPy-tris Board Watcher\n\n")

    # 盤面を出力する分の行数を確保する
    for _ in range(DISPLAYED_BOARD_HEIGHT):
        print("", flush=True)
    
    # boardオブジェクトの生成
    board = Board()

    # メインループ
    while True:
        a = Timer()
        board.currentMino = boardWatcher.GetCurrentMino()
        board.mainBoard = boardWatcher.GetMainBoard()
        board.followingMinos = boardWatcher.GetFollowingMinos()
        board.holdMino = boardWatcher.GetHoldMino()
        if board.currentMino is not None:
            PrintBoardWithDirectedMino(board, board.currentMino, True, a.Stop())
        else:
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

    board.minoBagContents = ReturnFullBag()
    for i in range(FOLLOWING_MINOS_COUNT):
        if board.followingMinos[i] is MINO.NONE:
            board.followingMinos[i] = board.minoBagContents.pop()
            if len(board.minoBagContents) == 0:
                board.minoBagContents = ReturnFullBag()

   
    print("\n\n\n")
    PrintBoard(board)

    """ # Decide
    while True:
        assert type(board.score) == int
        assert len(board.followingMinos) == FOLLOWING_MINOS_COUNT
        board = simulator.AddFollowingMino(board)

        # 思考ルーチン
        value, mino, path = decisionMaker.Decide(board)

        board, isTspin, isTspinmini = simulator.PutMino(path, board)

        newMainBoard, newTopRowIdx, clearedRowCount = simulator.ClearLinesOfBoard(board)
        scoreAdd, backToBack, ren = evaluator.Score(isTspin, isTspinmini, clearedRowCount, board.backToBack, board.ren)

        board = Board(
            newMainBoard,
            None,
            board.followingMinos,
            board.holdMino,
            True,
            newTopRowIdx,
            board.score + scoreAdd,
            backToBack,
            ren,
            board.minoBagContents
        )
    """
    
    # Multi-Decide
    board = simulator.AddFollowingMino(board)
    while True:
        assert type(board.score) == int
        assert len(board.followingMinos) == FOLLOWING_MINOS_COUNT

        # 思考ルーチン
        multipath = decisionMaker.MultiDecide(board)

        for path in multipath:
            board, isTspin, isTspinmini = simulator.PutMino(path, board)

            newMainBoard, newTopRowIdx, clearedRowCount = simulator.ClearLinesOfBoard(board)
            scoreAdd, backToBack, ren = evaluator.Score(isTspin, isTspinmini, clearedRowCount, board.backToBack, board.ren)

            board = Board(
                newMainBoard,
                None,
                board.followingMinos,
                board.holdMino,
                True,
                newTopRowIdx,
                board.score + scoreAdd,
                backToBack,
                ren,
                board.minoBagContents
            )

            board = simulator.AddFollowingMino(board)


# 実機上で思考を再現する（無限ループ、シングルスレッド）
# menu画面にいて、Startを押せる状態からはじめないとバグる
def PytrisMover ():
    # # マルチプレイヤーモード

    # # sが押されるまで待機
    # import keyboard
    # print("Press 's' to start.")
    # while True:
    #     if keyboard.read_key() == "s":
    #         PressEnter()
    #         time.sleep(0.5)
    #         Move(MOVE.RIGHT)
    #         time.sleep(0.5)
    #         PressEnter()
    #         time.sleep(0.5)
    #         PressEnter() # キャラ設定完了
    #         time.sleep(3)
    #         PressEnter() # ゲーム開始
    #         time.sleep(10)
    #         break

    # シングルプレイヤーモード
    
    # ゲームの再開
    PressEnter()

    time.sleep(4) # todo: 開始までただ待つのではなく、メモリ読み込みで開始したことを取得できるようにする

    # # 盤面を出力する分の行数を確保する
    # for _ in range(DISPLAYED_BOARD_HEIGHT):
    #     print("", flush=True)
    
    previousFollowingMinos = [boardWatcher.GetFollowingMinos()[0]]

    while True:
        # 消去中のラインが消えるまで待つ
        while boardWatcher.IsClearingLines():
            pass

        # followingMinosが変化するまで待つ
        while True:
            if previousFollowingMinos != boardWatcher.GetFollowingMinos():
                currentMino = previousFollowingMinos[0]
                previousFollowingMinos = boardWatcher.GetFollowingMinos()
                break
        
        # 各列において，上から順に見ていって，一番最初にブロックがある部分のrowIdxを格納する
        mainBoard = boardWatcher.GetMainBoard()
        topRowIdx = [BOARD_HEIGHT for _ in range(BOARD_WIDTH)]
        for rowIdx in range(BOARD_HEIGHT-1, -1, -1):
            for colIdx in range(BOARD_WIDTH):
                if mainBoard[rowIdx] & (0b1000000000 >> colIdx) > 0:
                    topRowIdx[colIdx] = rowIdx
        
        # 盤面の状況を読み取る
        board = Board(
            mainBoard,
            DirectedMino(
                currentMino, # ここで仮にGetCurrentMinoをやるとminoの種類が正しくないものが入ってきてしまう（おそらくメモリに反映されるのに時間がかかるため？）
                FIRST_MINO_DIRECTION,
                FIRST_MINO_POS
            ),
            boardWatcher.GetFollowingMinos(),
            boardWatcher.GetHoldMino(),
            True,
            topRowIdx,
            0,
            False,
            0
        )

        # PrintBoard(board, True)
        
        # 思考ルーチン
        value, mino, path = decisionMaker.Decide(board)

        # 移動
        directedMino = minoMover.InputMove(
            path,
            DirectedMino(
                currentMino, # ここで仮にGetCurrentMinoをやるとdecideで時間がかかっていたときに高さが合わなくなって死ぬ
                FIRST_MINO_DIRECTION,
                FIRST_MINO_POS
            ),
            board.mainBoard
        )

def main():    
    # # 盤面監視モード
    # PytrisBoardWatcher()

    # # # simulatorモード
    PytrisSimulator()

    # 実機確認モード
    # PytrisMover()
