from lib import *

try:
    from pymem import *
    from pymem.process import *
    mem = Pymem("puyopuyotetris.exe")
    module = module_from_name(mem.process_handle, "puyopuyotetris.exe").lpBaseOfDll
except:
    pass

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

# 盤面においてクリア中のラインがあるかどうか判定
# 一列すべて揃っているブロックがある（まだクリア判定されていない）か (実装todo)、0xFFFFFFFEが存在するか、空中に浮いているブロックがあるときまだラインのクリア中であると判定する
def IsClearingLines() -> bool:
    notEmptyRowFound = False
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
                if mino == 0xFFFFFFFE:
                    return True
                if mino >= 0:
                    row |= 0b1000000000 >> j
            except:
                pass
        if row != 0:
            notEmptyRowFound = True
        if notEmptyRowFound and row == 0: # 宙に浮いている行がある
            return True
    return False

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

# 現在のミノの位置を取得
def GetPosOfCurrentMino() -> Union[Tuple[int], None]:
    try: # todo: エラー処理
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
        return (x,y)
    except:
        return None

# 現在のミノの種類を取得
def GetMinoTypeOfCurrentMino() -> Union[MINO, None]:
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
        else:
            return None
    except:
        return None

# 現在のミノの方向を取得
def GetDirectionOfCurrentMino() -> Union[DIRECTION, None]:
    try: # todo: エラー処理
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
            return DIRECTION.N
        elif direction == 1:
            return DIRECTION.E
        elif direction == 2:
            return DIRECTION.S
        elif direction == 3:
            return DIRECTION.W
        else:
            return None
    except:
        return None

# 現在のミノを取得
def GetCurrentMino() -> Union[DirectedMino, None]:
    mino = GetMinoTypeOfCurrentMino()
    pos = GetPosOfCurrentMino()
    direction = GetDirectionOfCurrentMino()
    if (
        mino is not None and
        pos is not None and
        direction is not None
    ):
        return DirectedMino(
            mino,
            direction,
            pos
        )
    else:
        return None
