from tkinter import W
from lib import *

from pymem import *
from pymem.process import *

mem = Pymem("puyopuyotetris.exe")
module = module_from_name(mem.process_handle, "puyopuyotetris.exe").lpBaseOfDll

def GetAddrFromBaseAndOffsets(baseAddr:int, offsets:List[int]) -> int:
    addr = mem.read_int(baseAddr)
    for offset in offsets[:-1]:
        addr = mem.read_int(addr + offset)
    return addr + offsets[-1]

# 1: next mino, 2: next next mino, ...
def GetFollowingMinos() -> List[MINO]:
    followingMinos = []
    for i in range(FOLLOWING_MINOS_COUNT):
        try: # todo: エラー処理
            mino = mem.read_int(GetAddrFromBaseAndOffsets(
                0x140461B20,
                [
                    0x378,
                    0xB8,
                    0x15C + 0x4 * i
                ]
            ))
            if mino == 0:
                followingMinos.append(MINO.S)
            elif mino == 1:
                followingMinos.append(MINO.Z)
            elif mino == 2:
                followingMinos.append(MINO.J)
            elif mino == 3:
                followingMinos.append(MINO.L)
            elif mino == 4:
                followingMinos.append(MINO.T)
            elif mino == 5:
                followingMinos.append(MINO.O)
            elif mino == 6:
                followingMinos.append(MINO.I)
        except:
            followingMinos.append(MINO.NONE)
    
    return followingMinos

# holdミノを返す
def GetHoldMino() -> MINO:
    try: # todo: エラー処理
        mino = mem.read_int(GetAddrFromBaseAndOffsets(
            0x140598a20,
            [
                0x38,
                0x3d0,
                0x8
            ]
        ))
        if mino == 0:
            return MINO.S
        elif mino == 1:
            return MINO.Z
        elif mino == 2:
            return MINO.J
        elif mino == 3:
            return MINO.L
        elif mino == 4:
            return MINO.T
        elif mino == 5:
            return MINO.O
        elif mino == 6:
            return MINO.I
    except:
        return MINO.NONE

# 盤面の状況を返す
def GetMainBoard() -> List[int]:
    # 盤面の色を判断する
    mainBoard = [0b0 for _ in range(BOARD_HEIGHT - DISPLAYED_BOARD_HEIGHT)]
    for i in range(DISPLAYED_BOARD_HEIGHT-1, -1, -1):
        row = 0b0
        for j in range(BOARD_WIDTH):
            try: # todo: エラー処理
                mino = mem.read_int(GetAddrFromBaseAndOffsets(
                    0x140461B20,
                    [
                        0x378,
                        0xA8,
                        0x3C0,
                        0x18,
                        0x8 * j,
                        0x4 * i
                    ]
                ))
                if mino >= 0:
                    row |= 0b1000000000 >> j
            except:
                pass
        mainBoard.append(row)
    
    return mainBoard

# 現在のミノを取得
def GetCurrentMino() -> Union[DirectedMino, None]:
    try: # todo: エラー処理
        mino = mem.read_int(GetAddrFromBaseAndOffsets(
            0x140461B20,
            [
                0x378,
                0xc0,
                0x120,
                0x110
            ]
        ))
        if mino == 0:
            mino = MINO.S
        elif mino == 1:
            mino = MINO.Z
        elif mino == 2:
            mino = MINO.J
        elif mino == 3:
            mino = MINO.L
        elif mino == 4:
            mino = MINO.T
        elif mino == 5:
            mino = MINO.O
        elif mino == 6:
            mino = MINO.I
        else:
            return None
        x = mem.read_int(GetAddrFromBaseAndOffsets(
            0x140461B20,
            [
                0x378,
                0xa8,
                0x3c8,
                0xc
            ]
        ))
        y = 39 - mem.read_int(GetAddrFromBaseAndOffsets(
            0x140461B20,
            [
                0x378,
                0xa8,
                0x3c8,
                0x10
            ]
        ))
        direction = mem.read_int(GetAddrFromBaseAndOffsets(
            0x140461B20,
            [
                0x378,
                0xa8,
                0x3c8,
                0x18
            ]
        ))
        if direction == 0:
            direction = DIRECTION.N
        elif direction == 1:
            direction = DIRECTION.E
        elif direction == 2:
            direction = DIRECTION.S
        elif direction == 3:
            direction = DIRECTION.W
        return DirectedMino(
            mino,
            direction,
            (x,y)
        )
    except:
        return None
