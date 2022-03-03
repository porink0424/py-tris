from lib.constants import *
from lib.classes.directedMino import *

class Board():
    def __init__(
        self,
        mainBoard : List[List[MINO]] = None,
        currentMino : Union[DirectedMino, None] = None,
        followingMinos : List[MINO] = None,
        holdMino : MINO = None,
        canHold:bool = True,
        minoBagContents : Union[List[MINO], None] = None
    ) -> None:
        self.mainBoard = mainBoard if mainBoard is not None else [[MINO.NONE for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.followingMinos = followingMinos if followingMinos is not None else [MINO.NONE for _ in range(FOLLOWING_MINOS_COUNT)]
        self.currentMino = currentMino if currentMino is not None else None
        self.holdMino = holdMino if holdMino is not None else MINO.NONE
        self.canHold = canHold
        self.minoBagContents = minoBagContents # ReturnFullBag()

    # mainBoardの任意の場所にブロックを足す
    def AddMinoToMainBoard (self, pos:Tuple[int], mino:MINO):
        self.mainBoard[pos[1]][pos[0]] = mino
    
    def DeleteMinoInMainBoard (self, pos:Tuple[int]):
        self.mainBoard[pos[1]][pos[0]] = MINO.NONE
