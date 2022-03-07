from lib import *
import minoMover
import evaluator

DISPLAY_DELTA_TIME = 0.02

# 1つのnowDirectedMinoを置く動きを再現して出力
# 返り値としておいた後のboardを返す
def PutMino (moveList:List[MOVE], nowDirectedMino:DirectedMino, board:Board) -> Tuple[Board, bool, bool]:
    # moveListに従って1つずつ動かしていく
    nextDirectedMino = nowDirectedMino
    for move in moveList:
        PrintBoardWithDirectedMino(board, nextDirectedMino, True)
        nextDirectedMino = minoMover.MoveOneStep(move, nextDirectedMino, board)
        time.sleep(DISPLAY_DELTA_TIME)
    
    # 最終状態の出力
    PrintBoardWithDirectedMino(board, nextDirectedMino, True)

    # debug: Tスピン時に音を鳴らす
    isTspin = evaluator.IsTSpin(board.mainBoard, nextDirectedMino, moveList)
    isTspinmini = evaluator.IsTSpinMini(board.mainBoard, nextDirectedMino, moveList)
    if isTspin:
        if isTspinmini:
            os.system("Say -v Samantha 'T spin mini'")
        else:
            os.system("Say -v Samantha 'T spin'")

    joinedMainBoard, joinedTopRowIdx = JoinDirectedMinoToBoard(nextDirectedMino, board.mainBoard, board.topRowIdx)
    return Board(
        joinedMainBoard,
        board.currentMino,
        board.followingMinos,
        board.holdMino,
        board.canHold,
        joinedTopRowIdx,
        board.score,
        board.backToBack,
        board.ren
    ), isTspin, isTspinmini

# ラインをクリアする
def ClearLinesOfBoard(board:Board) -> Tuple[List[List[MINO]], int]:
    newMainBoard, newTopRowIdx, clearedRowCount = ClearLines(board.mainBoard, board.topRowIdx)
    time.sleep(DISPLAY_DELTA_TIME)
    PrintBoard(Board(
        newMainBoard,
        board.currentMino,
        board.followingMinos,
        board.holdMino,
        board.canHold,
        newTopRowIdx,
        board.score,
        board.backToBack,
        board.ren
    ), True, None, False, True)
    time.sleep(DISPLAY_DELTA_TIME)
    return newMainBoard, newTopRowIdx, clearedRowCount

# 次のミノを付け足し，押し出してネクストのミノをcurrentMinoにする
def AddFollowingMino (board:Board, addedMino:MINO) -> Board:
    return Board(
        board.mainBoard,
        DirectedMino(
            board.followingMinos[0],
            FIRST_MINO_DIRECTION,
            FIRST_MINO_POS
        ),
        board.followingMinos[1:] + [addedMino],
        board.holdMino,
        True,
        board.topRowIdx,
        board.score,
        board.backToBack,
        board.ren
    )

# 7種1巡の法則に従ってランダムでミノを生成する
bags = []
def GenerateMino () -> MINO:
    global bags

    # bagsが空であれば，7種類のミノをランダムに生成してbagsに入れる
    if not bags:
        bags = random.sample([
            MINO.I,
            MINO.J,
            MINO.L,
            MINO.O,
            MINO.S,
            MINO.T,
            MINO.Z
        ], 7)
    
    return bags.pop()
