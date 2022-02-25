from lib.constants.mino import *

# DIRECTION.Nを向いているときのミノの形を縦2*横4のボックスで表す
SHAPE = {
    MINO.I : [
        [0,0,0,0],
        [1,1,1,1]
    ],
    MINO.O : [
        [1,1,0,0],
        [1,1,0,0]
    ],
    MINO.T : [
        [0,1,0,0],
        [1,1,1,0]
    ],
    MINO.S : [
        [0,1,1,0],
        [1,1,0,0],
    ],
    MINO.Z : [
        [1,1,0,0],
        [0,1,1,0]
    ],
    MINO.L : [
        [0,0,1,0],
        [1,1,1,0],
    ],
    MINO.J : [
        [1,0,0,0],
        [1,1,1,0]
    ],
    MINO.NONE : [
        [0,0,0,0],
        [0,0,0,0]
    ]
}

SHAPE_WIDTH = 4
SHAPE_HEIGHT = 2