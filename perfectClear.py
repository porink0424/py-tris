from lib import *
from enum import Enum, auto




class PCState(Enum):
    FirstSZTLeft = auto()
    FirstSZTRight = auto()
    Second = auto()
    Wait = auto()



pcState = PCState.Wait
pcReturnValueQueue = [] # 返り値キュー




def AssignPCMinoMoves(
        minos:List[MINO], 
        tMove:List[MOVE],
        oMove:List[MOVE],
        zMove:List[MOVE],
        iMove:List[MOVE],
        lMove:List[MOVE],
        sMove:List[MOVE],
        jMove:List[MOVE]
    ) -> List[Tuple[DirectedMino, List[MOVE]]]:
    minoBag = ReturnFullBag()
    pcReturnValueQueue = []
    for i,nextMino in enumerate(minos):
        minoBag.remove(nextMino)
        pcReturnValueQueue.append( ReturnCorrespondingMinoMove(nextMino, tMove, oMove, zMove, iMove, lMove, sMove, jMove) )
    pcReturnValueQueue.append( ReturnCorrespondingMinoMove(minoBag[0], tMove, oMove, zMove, iMove, lMove, sMove, jMove) )
    return pcReturnValueQueue

def ReturnCorrespondingMinoMove(
        mino:MINO,
        tMove:List[MOVE],
        oMove:List[MOVE],
        zMove:List[MOVE],
        iMove:List[MOVE],
        lMove:List[MOVE],
        sMove:List[MOVE],
        jMove:List[MOVE]
    ) -> List[MOVE]:
    if mino is MINO.T:
        return tMove
    elif nextMino is MINO.O:
        return oMove
    elif nextMino is MINO.Z:
        return zMove
    elif nextMino is MINO.I:
        return iMove
    elif nextMino is MINO.L:
        return lMove
    elif nextMino is MINO.S:
        return sMove
    elif nextMino is MINO.J:
        return jMove


# CAUTION: ミノの左右移動を埋め込みにしている部分あり
def PerfectClear(board:Board) -> List[Tuple[DirectedMino, List[MOVE]]]:

    global pcState
    global pcReturnValueQueue

    if pcReturnValueQueue: # pcState is not PCState.Wait
        # 返り値キューが空でなければ思考済みなので前から取って返すだけ
        return (board.currentMino, pcReturnValueQueue.pop(0)) #FIXME: hold 非対応

    elif pcState is PCState.Wait:
        minoOrder = CheckMinoOrder(board.currentMino.mino, board.followingMinos)

        if (len(board.minoBagContents) == 7) and isBoardTopAligned(board.mainBoard):
            # 一巡目のパフェ積みが可能

            #----- hold 可否を判断 -----#
            if board.holdMino is MINO.NONE:
                canHoldInPC = True
            else:
                canHoldInPC = False
            # tHold = minoOrder.SZ_T
            # oHold = minoOrder.O_LJ and not (minoOrder.SZ_T and minoOrder.OT)
            # iHold = (not tHold and not oHold) or () or () # そもそも他に hold が必要ないか，他の hold 解消後だったら，hold してよい FIXME
            iHold = canHoldInPC
            # SZT/ZST では，T が来たら Z/S の hold 解消
            # OLJ なら，L が来たら O の hold 解消
            # OLJ なら，J が来たら O の hold 解消

            #----- 積み方の左右を決定 -----#
            if minoOrder.SZ:
                # SZT が左側にくるタイプで進める
                pcState = PCState.FirstSZTLeft
            else:
                # SZT が右側にくるタイプで進める
                pcState = PCState.FirstSZTRight

            #----- でこぼこ側 (SZT) -----#
            if minoOrder.SZ: # SZT or STZ or TSZ
                zMove = [MOVE.LEFT, MOVE.LEFT, MOVE.LEFT, MOVE.DROP]
                tMove = [MOVE.R_ROT, MOVE.LEFT, MOVE.LEFT, MOVE.LEFT, MOVE.LEFT, MOVE.DROP]
                if not minoOrder.ST: # TSZ
                    # S をハードドロップできない
                    sMove = [MOVE.LEFT] + [MOVE.DOWN for _ in range(alignedBoardTop - FIRST_MINO_POS[1] - 1)] + [MOVE.LEFT]
                else: # SZT or STZ
                    # S をハードドロップ可能
                    sMove = [MOVE.LEFT, MOVE.LEFT, MOVE.DROP]
                    if minoOrder.ZT: # SZT
                        # Z をホールドする必要がある
                        pcState = PCState.Wait
                        pcReturnValueQueue = []
                        return [] # TODO: hold
            else: # ZST or ZTS or TZS
                sMove = [MOVE.RIGHT, MOVE.RIGHT, MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
                tMove = [MOVE.L_ROT, MOVE.RIGHT, MOVE.RIGHT, MOVE.RIGHT, MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
                if not minoOrder.ZT: # TZS
                    # Z をハードドロップできない
                    zMove = [MOVE.RIGHT, MOVE.RIGHT] + [MOVE.DOWN for _ in range(alignedBoardTop - FIRST_MINO_POS[1] - 1)] + [MOVE.RIGHT]
                else: # ZST or ZTS
                    # Z をハードドロップ可能
                    zMove = [MOVE.RIGHT, MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
                    if minoOrder.ST: # ZST
                        # S をホールドする必要がある
                        pcState = PCState.Wait
                        pcReturnValueQueue = []
                        return [] # TODO: hold

            #----- 長方形側 (OLJ,I) -----#
            if minoOrder.O_LJ: # OLJ or OJL
                # TODO: hold
                pcState = PCState.Wait
                pcReturnValueQueue = []
                return [] # TODO
            else:
                # O の動き
                if not minoOrder.OL and not minoOrder.OJ: # LJO or JLO
                    # O をハードドロップできない
                    oMove = [MOVE.DOWN for _ in range(alignedBoardTop - FIRST_MINO_POS[1] - 1 - 1)] + [MOVE.RIGHT, MOVE.RIGHT]
                    # oMove = [MOVE.DOWN for _ in range(alignedBoardTop - FIRST_MINO_POS[1] - 1 - 1)] + [MOVE.RIGHT, MOVE.RIGHT, MOVE.RIGHT]
                else: # JOL or LOJ
                    # O をハードドロップ可能
                    oMove = [MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
                    # oMove = [MOVE.RIGHT, MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
                # SZT が右側の場合は O の動きを鏡映にする
                if not minoOrder.SZ:
                    oMove = ReflectMoves(oMove)

                # L,J の動き
                if minoOrder.LJ: # LJO or LOJ
                    if minoOrder.SZ:
                        lMove = [MOVE.RIGHT, MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
                        jMove = [MOVE.R_ROT, MOVE.R_ROT, MOVE.RIGHT, MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
                    else:
                        if minoOrder.OJ:
                            lMove = [MOVE.LEFT, MOVE.LEFT, MOVE.DROP]
                            jMove = [MOVE.R_ROT, MOVE.R_ROT, MOVE.LEFT, MOVE.LEFT, MOVE.DROP]
                        else:
                            pcState = PCState.Wait
                            pcReturnValueQueue = []
                            return [] # TODO
                else: # JLO or JOL
                    if not minoOrder.SZ:
                        lMove = [MOVE.R_ROT, MOVE.R_ROT, MOVE.LEFT, MOVE.LEFT, MOVE.DROP]
                        jMove = [MOVE.LEFT, MOVE.LEFT, MOVE.DROP]
                    else:
                        if minoOrder.OL:
                            lMove = [MOVE.R_ROT, MOVE.R_ROT, MOVE.RIGHT, MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
                            jMove = [MOVE.RIGHT, MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
                        else:
                            pcState = PCState.Wait
                            pcReturnValueQueue = []
                            return [] # TODO

                # I の動き
                iMove = [MOVE.L_ROT, MOVE.RIGHT, MOVE.RIGHT, MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
                if not minoOrder.SZ:
                    iMove = ReflectMoves(iMove)

            pcReturnValueQueue = AssignPCMinoMoves(
                board.currentMino.mino + board.followingMinos,
                tMove, oMove, zMove, iMove, lMove, sMove, jMove
            )
            return (board.currentMino, pcReturnValueQueue.pop(0))

    # elif pcState is PCState.
    else:
        # あきらめて帰る
        pcState = PCState.Wait
        pcReturnValueQueue = []
        return []


# https://harddrop.com/wiki/Perfect_Clear_Opener
# https://tannsokumegane.com/tetris-perfectclear/
# https://tetrisopener.wicurio.com/index.php?%E9%96%8B%E5%B9%95%E3%83%91%E3%83%95%E3%82%A7%E7%A9%8D%E3%81%BF
