from lib.constants import *
from lib.classes.directedMino import *

class Board():
    def __init__(
        self,
        mainBoard : List[int] = None,
        currentMino : Union[DirectedMino, None] = None,
        followingMinos : List[MINO] = None,
        holdMino : MINO = None,
        canHold:bool = True,
        minoBagContents : Union[List[MINO], None] = None
    ) -> None:
        self.mainBoard = mainBoard if mainBoard is not None else [0x0 for _ in range(BOARD_HEIGHT)]
        self.followingMinos = followingMinos if followingMinos is not None else [MINO.NONE for _ in range(FOLLOWING_MINOS_COUNT)]
        self.currentMino = currentMino
        self.holdMino = holdMino if holdMino is not None else MINO.NONE
        self.canHold = canHold
        self.minoBagContents = minoBagContents

    # mainBoardの任意の場所にブロックを足す
    def AddBlockToMainBoard (self, pos:Tuple[int]):
        self.mainBoard[pos[1]] |= 0b1000000000 >> pos[0]
    
    def DeleteBlockInMainBoard (self, pos:Tuple[int]):
        self.mainBoard[pos[1]] &= 0b1111111111 ^ (0b1000000000 >> pos[0])
