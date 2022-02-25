from lib import *
import minoMover
import evaluator

DISPLAY_DELTA_TIME = 0.02

# 1つのnowDirectedMinoを置く動きを再現して出力
# 返り値としておいた後のboardを返す
def PutMino (moveList:List[MOVE], nowDirectedMino:DirectedMino, board:Board) -> Board:
    # moveListに従って1つずつ動かしていく
    nextDirectedMino = nowDirectedMino
    for move in moveList:
        PrintBoardWithColorWithDirectedMino(board, nextDirectedMino, True)
        nextDirectedMino = minoMover.MoveOneStep(move, nextDirectedMino, board)
        time.sleep(DISPLAY_DELTA_TIME)
    
    # 最終状態の出力
    PrintBoardWithColorWithDirectedMino(board, nextDirectedMino, True)

    # debug: Tスピン時に音を鳴らす
    if evaluator.IsTSpin(board.mainBoard, nextDirectedMino, moveList[-2:]):
        if evaluator.IsTSpinMini(board.mainBoard, nextDirectedMino, moveList[-2:]):
            os.system("Say -v Samantha 'T spin mini'")
        else:
            os.system("Say -v Samantha 'T spin'")

    return JoinDirectedMinoToBoard(nextDirectedMino, board)

# ラインをクリアする
def ClearLinesOfBoard(board:Board) -> Tuple[List[List[MINO]], int]:
    newMainBoard, clearedRowCount = ClearLines(board.mainBoard)
    time.sleep(DISPLAY_DELTA_TIME)
    PrintBoardWithColor(Board(
        newMainBoard,
        board.currentMino,
        board.followingMinos,
        board.holdMino,
        board.canHold,
    ), True)
    time.sleep(DISPLAY_DELTA_TIME)
    return newMainBoard, clearedRowCount

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
        True
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
