from lib.constants import *
from lib.classes.directedMino import *

class Board():
    def __init__(
        self,
        mainBoard : List[int] = None,
        currentMino : Union[DirectedMino, None] = None,
        followingMinos : List[MINO] = None,
        holdMino : MINO = None,
        canHold : bool = True,
        topRowIdx : List[int] = None,
        score : int = 0,
        backToBack : bool = False,
        ren : int = 0,
        minoBagContents : Union[List[MINO], None] = None
    ) -> None:INO.ainBoard (self, pos:Tuple[int]):
        self.mainBoard[pos[1]] |= 0b1000000000 >> pos[0]
        self.topRowIdx[pos[0]] = min(self.topRowIdx[pos[0]], pos[1])
    
    def DeleteBlockInMainBoard (self, pos:Tuple[int]):
        self.mainBoard[pos[1]] &= 0b1111111111 ^ (0b1000000000 >> pos[0])
        if pos[1] == self.topRowIdx[pos[0]]:
            for rowIdx in range(pos[1], BOARD_HEIGHT):
                if (self.mainBoard[rowIdx] & (0b1000000000 >> pos[0])) > 0:
                    self.topRowIdx[pos[0]] = rowIdx
                    break
            else:
                self.topRowIdx[pos[0]] = BOARD_HEIGHT