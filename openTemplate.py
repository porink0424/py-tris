from lib import *
import decisionMaker

class Template:
    def __init__(self, minos:List[DirectedMino]):
        self.minos = minos 
        self.occcupiedPositions = [GetOccupiedPositions(mino) for mino in minos]

    def contain(self, occupiedPos:List[Tuple[int]]):
        for pos in self.occcupiedPositions:
            match = True 
            for pos_i, occupiedPos_i in zip(pos, occupiedPos):
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

"""
テンプレートを作る時、活用

-> x
|
v
y

MINO.L
   N     E   S   W
    #   #   #@# ##
  #@#   @   #    @
        ##       #

MINO.I
    N     E  S    W
   #@##   #  @    #
         @# ####  @
          #       #
          #       #

MINO.Z
   N     E    S    W
  ##     #   #@     #
   @#   @#    ##   #@
        #          #

MINO.S
   N    E     S    W
   ##   #     @#   #
  #@    @#   ##    #@
         #          #

MINO.J
   N    E    S    W
  #     ##  #@#   #
  #@#   @     #   @
        #        ##

MINO.O
  ##
  @#

MINO.T
   N    E     S     W 
   #    #    #@#    #
  #@#   @#    #    #@
        #           #
""" 

# テンプレートが盤面に再現されていかどうか判定
def tempalteOnMainBoard(template:Template, mainBoard:List[int]) -> bool:
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

            for mino, path, pos in moves:
                if template.contain(pos):
                    joindBoard, joinedTopRowIdx = JoinDirectedMinoToBoard(mino, board.mainBoard, board.topRowIdx)
                    newMainBoard, newTopRowIdx, _ = ClearLines(joindBoard, joinedTopRowIdx)
                    nextBoard = board
                    if path[0] is MOVE.HOLD:
                        nextBoard = BoardAfterHold(board)

                    nextBoard = Board(
                        newMainBoard,
                        DirectedMino(
                            nextBoard.followingMinos[0],
                            FIRST_MINO_DIRECTION,
                            FIRST_MINO_POS
                        ),
                        nextBoard.followingMinos[1:] + [MINO.NONE],
                        nextBoard.holdMino,
                        True,
                        newTopRowIdx,
                        nextBoard.score,
                        nextBoard.backToBack,
                        nextBoard.ren,
                        nextBoard.minoBagContents
                    )

                    nextBoards.append((nextBoard, accumPath + [path]))
        
        if len(nextBoards) == 0:
            for board, accumPath in boards:
                if tempalteOnMainBoard(template, board.mainBoard):
                    return accumPath
            return []
        else:
            boards = nextBoards

    if len(boards) > 0:
        return boards[0][1]
    else:
        return [] 

### TSD - templates
TSD1 = Template([DirectedMino(MINO.L, DIRECTION.E, (0, 38)),
                DirectedMino(MINO.I, DIRECTION.N, (4, 39)),
                DirectedMino(MINO.Z, DIRECTION.N, (4, 38)),
                DirectedMino(MINO.S, DIRECTION.W, (7, 38)),
                DirectedMino(MINO.J, DIRECTION.S, (4, 36)),
                DirectedMino(MINO.O, DIRECTION.N, (8, 39))])

TSD2 = Template([DirectedMino(MINO.L, DIRECTION.E, (0, 38)),
                DirectedMino(MINO.I, DIRECTION.N, (4, 39)),
                DirectedMino(MINO.Z, DIRECTION.N, (5, 37)),
                DirectedMino(MINO.S, DIRECTION.W, (4, 37)),
                DirectedMino(MINO.J, DIRECTION.S, (6, 38)),
                DirectedMino(MINO.O, DIRECTION.N, (8, 39))]) 

TSD3 = Template([DirectedMino(MINO.L, DIRECTION.S, (5, 36)),
                DirectedMino(MINO.I, DIRECTION.N, (4, 39)),
                DirectedMino(MINO.Z, DIRECTION.E, (2, 38)),
                DirectedMino(MINO.S, DIRECTION.N, (5, 38)),
                DirectedMino(MINO.J, DIRECTION.W, (9, 38)),
                DirectedMino(MINO.O, DIRECTION.N, (0, 39))]) 

TSD4 = Template([DirectedMino(MINO.L, DIRECTION.S, (3, 38)),
                DirectedMino(MINO.I, DIRECTION.N, (4, 39)),
                DirectedMino(MINO.Z, DIRECTION.E, (5, 37)),
                DirectedMino(MINO.S, DIRECTION.N, (4, 37)),
                DirectedMino(MINO.J, DIRECTION.W, (9, 38)),
                DirectedMino(MINO.O, DIRECTION.N, (0, 39))]) 

def GetTSDMove(board:Board):
    move1 = GetTemplateMove(board, TSD1)
    if len(move1) > 0:
        return move1 
    
    move2 = GetTemplateMove(board, TSD2)
    if len(move2) > 0:
        return move2

    move3 = GetTemplateMove(board, TSD3)
    if len(move3) > 0:
        return move3

    move4 = GetTemplateMove(board, TSD4)
    if len(move4) > 0:
        return move4

    return []

        
