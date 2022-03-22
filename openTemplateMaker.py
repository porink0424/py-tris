from lib import *
import decisionMaker

class Template:
    def __init__(self, minos:List[DirectedMino], noBlankRow:List[int]):
        # minosはテンプレートに含まれるミノ
        # noBlankRowはそのテンプレートを構成する途中でブロックの下の空白があってはならない行番号
        self.minos = minos 
        self.occcupiedPositions = [GetOccupiedPositions(mino) for mino in minos]
        self.noBlankrow = noBlankRow

    def contain(self, occupiedPositions:List[Tuple[int]]):
        for pos in self.occcupiedPositions:
            match = True 
            for pos_i, occupiedPos_i in zip(pos, occupiedPositions):
                if pos_i != occupiedPos_i:
                    match = False 
                    break
            if match:
                return True

        return False
    
    # 確認用
    # 新しいテンプレートを作った時はprintして自分の考えているものと一致しているかチェックする。
    def __str__(self):
        board = [[MINO.NONE for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        for mino in self.minos:
            pos = GetOccupiedPositions(mino)
            for pos0, pos1 in pos:
                if board[pos1][pos0] is not MINO.NONE:
                    Warn("cross mino!")
                board[pos1][pos0] = mino.mino 
        
        boardStr = [['.' for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                if board[i][j] is MINO.T:
                    boardStr[i][j] = 'T'
                elif board[i][j] is MINO.I:
                    boardStr[i][j] = 'I'
                elif board[i][j] is MINO.S:
                    boardStr[i][j] = 'S'
                elif board[i][j] is MINO.J:
                    boardStr[i][j] = 'J'
                elif board[i][j] is MINO.L:
                    boardStr[i][j] = 'L'
                elif board[i][j] is MINO.O:
                    boardStr[i][j] = 'O'
                elif board[i][j] is MINO.Z:
                    boardStr[i][j] = 'Z'

        return "\n".join(map(lambda x : "".join(x),boardStr))


# テンプレートが盤面に再現されていかどうか判定
def ExistsTemplateOnMainBoard(template:Template, mainBoard:List[int]) -> bool:
    for pos in template.occcupiedPositions:
        for pos0, pos1 in pos:
            if mainBoard[pos1] & (0b1000000000 >> pos0) == 0:
                return False 
    return True

# 第2引数のtemplateに対応するMOVEが存在するならそれを返す。
def GetTemplateMove(board:Board, template:Template) -> List[List[MoveInt]]:

    boards = [(board, [])]
    for _ in range(decisionMaker.SEARCH_LIMIT):
        nextBoards = []
        for board, accumPath in boards:
            moves = [(mino, path, GetOccupiedPositions(mino)) for mino, path in decisionMaker.GetNextMoves(board)]

            for mino, path, positions in moves:
                if template.contain(positions):
                    # ラインの消去
                    joindBoard, joinedTopRowIdx = JoinDirectedMinoToBoard(mino, board.mainBoard, board.topRowIdx)
                    newMainBoard, newTopRowIdx, _ = ClearLines(joindBoard, joinedTopRowIdx)

                    # boardAfterHoldは
                    # もしHoldをしていたらその操作だけ行った後の盤面
                    # そうではないときは元の盤面
                    boardAfterHold = board
                    if path[0] is MOVE.HOLD:
                        boardAfterHold = BoardAfterHold(board)

                    nextBoard = Board(
                        newMainBoard,
                        DirectedMino(
                            boardAfterHold.followingMinos[0],
                            FIRST_MINO_DIRECTION,
                            FIRST_MINO_POS
                        ),
                        boardAfterHold.followingMinos[1:] + [MINO.NONE],
                        boardAfterHold.holdMino,
                        True,
                        newTopRowIdx,
                        boardAfterHold.score,
                        boardAfterHold.backToBack,
                        boardAfterHold.ren,
                        boardAfterHold.minoBagContents
                    )

                    nextBoards.append((nextBoard, accumPath + [path]))
        
        if not nextBoards:
            for board, accumPath in boards:
                if ExistsTemplateOnMainBoard(template, board.mainBoard):
                    return accumPath
            return []
        else:
            boards = nextBoards

    if boards:
        for board, path in boards:

            # ブロックの下に空白がある時は将来的にこのテンプレを実行できない可能性が高い
            blank = False
            for i in template.noBlankrow:
                for j in range(board.topRowIdx[i], BOARD_HEIGHT):
                    if (board.mainBoard[j] & (0b1000000000 >> i) == 0):
                        blank = True
                        break
                if blank:
                    break

            if not blank:
                return path

        return []              
    else:
        return [] 

### TSD - templates
TSD1 = Template([DirectedMino(MINO.L, DIRECTION.E, (0, 38)),
                DirectedMino(MINO.I, DIRECTION.N, (4, 39)),
                DirectedMino(MINO.Z, DIRECTION.N, (4, 38)),
                DirectedMino(MINO.S, DIRECTION.W, (7, 38)),
                DirectedMino(MINO.J, DIRECTION.S, (4, 36)),
                DirectedMino(MINO.O, DIRECTION.N, (8, 39))],
                [])

TSD2 = Template([DirectedMino(MINO.L, DIRECTION.E, (0, 38)),
                DirectedMino(MINO.I, DIRECTION.N, (4, 39)),
                DirectedMino(MINO.Z, DIRECTION.N, (5, 37)),
                DirectedMino(MINO.S, DIRECTION.W, (4, 37)),
                DirectedMino(MINO.J, DIRECTION.S, (6, 38)),
                DirectedMino(MINO.O, DIRECTION.N, (8, 39))],
                []) 

TSD3 = Template([DirectedMino(MINO.L, DIRECTION.S, (5, 36)),
                DirectedMino(MINO.I, DIRECTION.N, (4, 39)),
                DirectedMino(MINO.Z, DIRECTION.E, (2, 38)),
                DirectedMino(MINO.S, DIRECTION.N, (5, 38)),
                DirectedMino(MINO.J, DIRECTION.W, (9, 38)),
                DirectedMino(MINO.O, DIRECTION.N, (0, 39))],
                []) 

TSD4 = Template([DirectedMino(MINO.L, DIRECTION.S, (3, 38)),
                DirectedMino(MINO.I, DIRECTION.N, (4, 39)),
                DirectedMino(MINO.Z, DIRECTION.E, (5, 37)),
                DirectedMino(MINO.S, DIRECTION.N, (4, 37)),
                DirectedMino(MINO.J, DIRECTION.W, (9, 38)),
                DirectedMino(MINO.O, DIRECTION.N, (0, 39))],
                []) 

def GetTSDMove(board:Board):
    move1 = GetTemplateMove(board, TSD1)
    if move1:
        return move1 
    
    move2 = GetTemplateMove(board, TSD2)
    if move2:
        return move2

    move3 = GetTemplateMove(board, TSD3)
    if move3:
        return move3

    move4 = GetTemplateMove(board, TSD4)
    if move4:
        return move4

    return []

### DT - template
DT11 = Template([DirectedMino(MINO.L, DIRECTION.E, (7, 38)),
                DirectedMino(MINO.I, DIRECTION.W, (6, 37)),
                DirectedMino(MINO.Z, DIRECTION.E, (3, 38)),
                DirectedMino(MINO.S, DIRECTION.E, (8, 38)),
                DirectedMino(MINO.J, DIRECTION.W, (5, 38)),
                DirectedMino(MINO.O, DIRECTION.N, (0, 39)),
                DirectedMino(MINO.T, DIRECTION.N, (4, 36) )],
                [4, 5, 7, 8])

DT12 = Template([DirectedMino(MINO.L, DIRECTION.N, (4, 39)),
                DirectedMino(MINO.I, DIRECTION.W, (6, 37)),
                DirectedMino(MINO.Z, DIRECTION.N, (8, 38)),
                DirectedMino(MINO.S, DIRECTION.N, (4, 38)),
                DirectedMino(MINO.J, DIRECTION.N, (8, 39)),
                DirectedMino(MINO.O, DIRECTION.N, (0, 39)),
                DirectedMino(MINO.T, DIRECTION.N, (4, 36) )],
                [])

DT21 = Template([DirectedMino(MINO.L, DIRECTION.W, (3, 34)),
                DirectedMino(MINO.I, DIRECTION.W, (9, 35)),
                DirectedMino(MINO.Z, DIRECTION.N, (5, 35)),
                DirectedMino(MINO.S, DIRECTION.E, (5, 33)),
                DirectedMino(MINO.J, DIRECTION.E, (0, 36)),
                DirectedMino(MINO.O, DIRECTION.N, (7, 36))],
                [])

DT22 = Template([DirectedMino(MINO.L, DIRECTION.W, (3, 34)),
                DirectedMino(MINO.I, DIRECTION.W, (9, 35)),
                DirectedMino(MINO.Z, DIRECTION.E, (6, 34)),
                DirectedMino(MINO.S, DIRECTION.E, (4, 34)),
                DirectedMino(MINO.J, DIRECTION.E, (0, 36)),
                DirectedMino(MINO.O, DIRECTION.N, (7, 36))],
                [])

DT23 = Template([DirectedMino(MINO.L, DIRECTION.W, (3, 34)),
                DirectedMino(MINO.I, DIRECTION.W, (9, 35)),
                DirectedMino(MINO.Z, DIRECTION.N, (7, 36)),
                DirectedMino(MINO.S, DIRECTION.E, (4, 34)),
                DirectedMino(MINO.J, DIRECTION.E, (0, 36)),
                DirectedMino(MINO.O, DIRECTION.N, (6, 34))],
                [])

DT3 = Template([DirectedMino(MINO.T, DIRECTION.S, (2, 37))],
                [])

def GetDTMove(board:Board) -> List[List[MoveInt]]:
    move1 = GetTemplateMove(board, DT11)
    if move1:
        return move1
    
    move2 = GetTemplateMove(board, DT12)
    if move2:
        return move2
    

    if ExistsTemplateOnMainBoard(DT11, board.mainBoard):
        return GetDT2Move(board)

    return []

def GetDT2Move(board:Board) -> List[List[MoveInt]]:
    move1 = GetTemplateMove(board, DT21)
    if move1:
        return move1

    move2 = GetTemplateMove(board, DT22)
    if move2:
        return move2

    move3 = GetTemplateMove(board, DT23)
    if move3:
        return move3

    if ExistsTemplateOnMainBoard(DT21, board.mainBoard):
        return GetDT3Move(board)

    return []

def GetDT3Move(board:Board) -> List[List[MoveInt]]:
    move = GetTemplateMove(board, DT3)
    return move


### Gassho TSD
GasshoTSD1 = Template([DirectedMino(MINO.L, DIRECTION.N, (8, 37)),
                    DirectedMino(MINO.I, DIRECTION.W, (0, 37)),
                    DirectedMino(MINO.Z, DIRECTION.E, (4, 38)),
                    DirectedMino(MINO.S, DIRECTION.E, (6, 38)),
                    DirectedMino(MINO.J, DIRECTION.E, (1, 37)),
                    DirectedMino(MINO.O, DIRECTION.N, (8, 39)),
                    DirectedMino(MINO.T, DIRECTION.N, (2, 39) )],
                    [7, 8, 9])

def GetGasshoTSDMove(board:Board):
    return GetTemplateMove(board, GasshoTSD1)
    
### Customize Template
def GetCustomTemplateMove(board:Board) -> List[List[MoveInt]]:

    # DT　
    multipath = GetDTMove(board)
    if multipath:
        return multipath

    # TSD
    multipath = GetTSDMove(board)
    if multipath:
        return multipath

    # Gassho TSD
    multipath = GetGasshoTSDMove(board)

    return multipath