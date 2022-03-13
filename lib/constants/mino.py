from enum import Enum, auto
from typing import List
import random

class MINO(Enum):
    T = 0
    O = 1
    Z = 2
    I = 3
    L = 4
    S = 5
    J = 6
    JAMA = 7
    NONE = 8

def ReturnFullBag() -> List[MINO]:
    return random.sample([MINO.T, MINO.O, MINO.Z, MINO.I, MINO.L, MINO.S, MINO.J], 7)
