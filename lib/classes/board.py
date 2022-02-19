from lib.constants import *

class Board():
    def __init__(
        self,
        mainBoard : List[List[MINO]] = None,
        followingMinos : List[MINO] = None,
        holdMino : MINO = None,
        canHold:bool = True
    ) -> None:
        self.mainBoard = mainBoard if mainBoard is not None else [[MINO.NONE for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.followingMinos = followingMinos if followingMinos is not None else [MINO.NONE for _ in range(FOLLOWING_MINOS_COUNT)]
        self.holdMino = holdMino if holdMino is not None else MINO.NONE
        self.canHold = canHold
    
    # mainBoardの任意の場所にブロックを足す
    def AddMinoToMainBoard (self, pos:Tuple[int], mino:MINO):
        self.mainBoard[pos[1]][pos[0]] = mino
    
    def DeleteMinoInMainBoard (self, pos:Tuple[int]):
        self.mainBoard[pos[1]][pos[0]] = MINO.NONE
