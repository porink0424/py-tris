from enum import Enum, auto
from typing import List

class MINO(Enum):
    T = auto()
    O = auto()
    Z = auto()
    I = auto()
    L = auto()
    S = auto()
    J = auto()
    JAMA = auto()
    NONE = auto()

def ReturnFullBag() -> List[MINO]:
    return [MINO.T, MINO.O, MINO.Z, MINO.I, MINO.L, MINO.S, MINO.J]