from lib import *
import decisionMaker



class PCState():
    Wait = 0
    FirstSZTLeft = 1
    FirstSZTRight = 2
    Second = 3



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
    elif mino is MINO.O:
        return oMove
    elif mino is MINO.Z:
        return zMove
    elif mino is MINO.I:
        return iMove
    elif mino is MINO.L:
        return lMove
    elif mino is MINO.S:
        return sMove
    elif mino is MINO.J:
        return jMove



tMove = []
oMove = []
zMove = []
iMove = []
lMove = []
sMove = []
jMove = []

# CAUTION: ミノの左右移動を埋め込みにしている部分あり
def PerfectClear(board:Board) -> List[List[MoveInt]]:

    global pcState
    global pcReturnValueQueue
    global tMove
    global oMove
    global zMove
    global iMove
    global lMove
    global sMove
    global jMove

    if pcReturnValueQueue: # pcState is not PCState.Wait
        # 返り値キューが空でなければ思考済みなので前から取って返すだけ
        return [pcReturnValueQueue.pop(0)]

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
            # I がOLJよりも最後かどうか判定


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
                        if minoOrder.OJ: # LOJ
                            lMove = [MOVE.LEFT, MOVE.LEFT, MOVE.DROP]
                            jMove = [MOVE.R_ROT, MOVE.R_ROT, MOVE.LEFT, MOVE.LEFT, MOVE.DROP]
                            oMove = [MOVE.LEFT, MOVE.LEFT, MOVE.LEFT, MOVE.DROP] # 変な向きになるので O の動きも変えておく
                        else:
                            pcState = PCState.Wait
                            pcReturnValueQueue = []
                            return [] # TODO
                else: # JLO or JOL
                    if not minoOrder.SZ:
                        lMove = [MOVE.R_ROT, MOVE.R_ROT, MOVE.LEFT, MOVE.LEFT, MOVE.DROP]
                        jMove = [MOVE.LEFT, MOVE.LEFT, MOVE.DROP]
                    else:
                        if minoOrder.OL: # JOL
                            lMove = [MOVE.R_ROT, MOVE.R_ROT, MOVE.RIGHT, MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
                            jMove = [MOVE.RIGHT, MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
                            oMove = [MOVE.RIGHT, MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP] # 変な向きになるので O の動きも変えておく
                        else:
                            pcState = PCState.Wait
                            pcReturnValueQueue = []
                            return [] # TODO

                # I の動き
                iMove = [MOVE.L_ROT, MOVE.RIGHT, MOVE.RIGHT, MOVE.RIGHT, MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
                if not minoOrder.SZ:
                    iMove = ReflectMoves(iMove)

            pcReturnValueQueue = AssignPCMinoMoves(
                [board.currentMino.mino] + board.followingMinos,
                tMove, oMove, zMove, iMove, lMove, sMove, jMove
            )
            return [pcReturnValueQueue.pop(0)]

    elif pcState in [PCState.FirstSZTRight, PCState.FirstSZTLeft]:
        pcState = PCState.Wait
        pcReturnValueQueue = SearchPCSecondMove(board, 3)
        if not pcReturnValueQueue:
            return []
        else:
            return [pcReturnValueQueue.pop(0)]

    #     threeMinos = [board.currentMino.mino, board.followingMinos[0], board.followingMinos[1]]
    #     threeMinosSet = set(threeMinos)

    #     # IITJ
    #     if threeMinosSet == {MINO.J, MINO.I, MINO.T}: # IITJ
    #         jMove = [MOVE.R_ROT] + [MOVE.DOWN for _ in range(alignedBoardTop - FIRST_MINO_POS[1] - 1)] + [MOVE.L_ROT]
    #         iMove = [MOVE.RIGHT, MOVE.DROP]
    #         tMove = [MOVE.R_ROT, MOVE.R_ROT, MOVE.RIGHT, MOVE.DROP]

    #     # IITL
    #     elif (
    #         threeMinos == [MINO.T, MINO.I, MINO.L] or 
    #         threeMinos == [MINO.T, MINO.L, MINO.I] or
    #         threeMinos == [MINO.I, MINO.T, MINO.L]
    #     ): # IITL
    #         tMove = [MOVE.R_ROT] + [MOVE.DOWN for _ in range(alignedBoardTop - FIRST_MINO_POS[1] - 1)] + [MOVE.L_ROT]
    #         iMove = [MOVE.RIGHT, MOVE.DROP]
    #         lMove = [MOVE.R_ROT, MOVE.R_ROT, MOVE.RIGHT, MOVE.DROP]
    #     elif (
    #         threeMinos == [MINO.L, MINO.I, MINO.T] or 
    #         threeMinos == [MINO.L, MINO.T, MINO.I]
    #     ): # IITL
    #         tMove = [MOVE.R_ROT, MOVE.R_ROT, MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
    #         iMove = [MOVE.L_ROT, MOVE.DROP] #FIXME
    #         lMove = [MOVE.R_ROT] + [MOVE.DOWN for _ in range(alignedBoardTop - FIRST_MINO_POS[1] - 1)] + [MOVE.RIGHT]

    #     # ITJS
    #     elif (
    #         threeMinos == [MINO.T, MINO.J, MINO.S] or 
    #         threeMinos == [MINO.T, MINO.S, MINO.J]
    #     ): # ITJS
    #         tMove = [MOVE.R_ROT] + [MOVE.DOWN for _ in range(alignedBoardTop - FIRST_MINO_POS[1] - 1 - 1)] + [MOVE.L_ROT, MOVE.DROP]
    #         jMove = [MOVE.R_ROT, MOVE.DROP]
    #         if threeMinos == [MINO.T, MINO.J, MINO.S]:
    #             sMove = [MOVE.R_ROT, MOVE.RIGHT] + [MOVE.DOWN for _ in range(alignedBoardTop - FIRST_MINO_POS[1] - 1 - 1)] + [MOVE.R_ROT, MOVE.DROP] # FIXME
    #         else:
    #             sMove = [MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
    #     elif threeMinos == [MINO.J, MINO.S, MINO.T]: # ITJS
    #         jMove = [MOVE.R_ROT] + [MOVE.DOWN for _ in range(alignedBoardTop - FIRST_MINO_POS[1] - 1)] + [MOVE.L_ROT]
    #         sMove = [MOVE.R_ROT, MOVE.DROP] #FIXME
    #         tMove = [MOVE.R_ROT, MOVE.R_ROT, MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]

    #     # IILZ
    #     elif (
    #         threeMinos == [MINO.Z, MINO.I, MINO.L] or 
    #         threeMinos == [MINO.Z, MINO.L, MINO.I] or
    #         threeMinos == [MINO.I, MINO.Z, MINO.L]
    #     ): # IILZ
    #         zMove = [MOVE.L_ROT, MOVE.RIGHT, MOVE.RIGHT] + [MOVE.DOWN for _ in range(alignedBoardTop - FIRST_MINO_POS[1] - 1 - 2)] + [MOVE.L_ROT]
    #         iMove = [MOVE.RIGHT, MOVE.DROP]
    #         lMove = [MOVE.R_ROT, MOVE.R_ROT, MOVE.RIGHT, MOVE.DROP]

    #     # IJSZ
    #     elif (
    #         threeMinos == [MINO.Z, MINO.J, MINO.S] or 
    #         threeMinos == [MINO.Z, MINO.S, MINO.J]
    #     ):
    #         zMove = [MOVE.R_ROT, MOVE.RIGHT] + [MOVE.DOWN for _ in range(alignedBoardTop - FIRST_MINO_POS[1] - 1 - 2)] + [MOVE.L_ROT]
    #         sMove = [MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
    #         jMove = [MOVE.R_ROT, MOVE.DROP]
    #     elif (
    #         threeMinos == [MINO.J, MINO.Z, MINO.S]
    #     ):
    #         jMove = [MOVE.RIGHT, MOVE.DROP]
    #         zMove = [MOVE.R_ROT, MOVE.DROP]
    #         sMove = [MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]

    #     # IITO
    #     elif (
    #         threeMinos == [MINO.I, MINO.T, MINO.O] or 
    #         threeMinos == [MINO.T, MINO.I, MINO.O] or 
    #         threeMinos == [MINO.T, MINO.O, MINO.I]
    #     ):
    #         tMove = [MOVE.R_ROT, MOVE.DROP]
    #         iMove = [MOVE.RIGHT, MOVE.DROP]
    #         oMove = [MOVE.RIGHT, MOVE.DROP]
            
    #     # IIOJ
    #     elif (
    #         threeMinos == [MINO.I, MINO.O, MINO.J] or 
    #         threeMinos == [MINO.O, MINO.I, MINO.J] or 
    #         threeMinos == [MINO.O, MINO.J, MINO.I]
    #     ):
    #         iMove = [MOVE.RIGHT, MOVE.DROP]
    #         oMove = [MOVE.DROP]
    #         jMove = [MOVE.R_ROT, MOVE.R_ROT, MOVE.RIGHT, MOVE.DROP]
            
    #     # IIJS
    #     elif (
    #         threeMinos == [MINO.I, MINO.S, MINO.J] or 
    #         threeMinos == [MINO.S, MINO.I, MINO.J] or 
    #         threeMinos == [MINO.S, MINO.J, MINO.I]
    #     ):
    #         iMove = [MOVE.RIGHT, MOVE.DROP]
    #         sMove = [MOVE.RIGHT, MOVE.DROP]
    #         jMove = [MOVE.RIGHT, MOVE.DROP]
            
    #     # IITS
    #     elif (
    #         threeMinos == [MINO.I, MINO.T, MINO.S] or 
    #         threeMinos == [MINO.T, MINO.I, MINO.S]
    #     ):
    #         iMove = [MOVE.L_ROT, MOVE.DROP]
    #         tMove = [MOVE.R_ROT, MOVE.RIGHT, MOVE.DROP]
    #         sMove = [MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
            
    #     # ITLJ
    #     elif (
    #         threeMinos == [MINO.T, MINO.J, MINO.L] or 
    #         threeMinos == [MINO.T, MINO.L, MINO.J]
    #     ):
    #         tMove = [MOVE.R_ROT, MOVE.DROP]
    #         lMove = [MOVE.L_ROT, MOVE.RIGHT, MOVE.DROP]
    #         jMove = [MOVE.L_ROT, MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
            
    #     # ITSZ
    #     elif (
    #         threeMinos == [MINO.T, MINO.S, MINO.Z] or
    #         threeMinos == [MINO.T, MINO.S, MINO.Z]
    #     ):
    #         tMove = [MOVE.R_ROT, MOVE.DROP]
    #         sMove = [MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
    #         zMove = [MOVE.RIGHT, MOVE.DROP]

    #     # IOJT
    #     elif (
    #         threeMinos == [MINO.O, MINO.J, MINO.T]
    #     ):
    #         oMove = [MOVE.DROP]
    #         jMove = [MOVE.RIGHT, MOVE.DROP]
    #         tMove = [MOVE.R_ROT, MOVE.R_ROT, MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]

    #     # else
    #     else:
    #         pcState = PCState.Wait
    #         pcReturnValueQueue = []
    #         return []
        
    #     # return
    #     pcReturnValueQueue = AssignPCMinoMoves(
    #         threeMinos,
    #         tMove, oMove, zMove, iMove, lMove, sMove, jMove
    #     )
    #     return [pcReturnValueQueue.pop(0)]

    # elif pcState is PCState.FirstSZTLeft:
    #     threeMinos = [board.currentMino.mino, board.followingMinos[0], board.followingMinos[1]]
    #     threeMinosSet = set(threeMinos)

    #     # IITJ
    #     if threeMinosSet == {MINO.L, MINO.I, MINO.T}: # IITJ
    #         lMove = [MOVE.L_ROT, MOVE.RIGHT] + [MOVE.DOWN for _ in range(alignedBoardTop - FIRST_MINO_POS[1] - 1)] + [MOVE.R_ROT]
    #         iMove = [MOVE.LEFT, MOVE.DROP]
    #         tMove = [MOVE.R_ROT, MOVE.R_ROT, MOVE.DROP]

    #     # IITL
    #     elif (
    #         threeMinos == [MINO.T, MINO.I, MINO.J] or 
    #         threeMinos == [MINO.T, MINO.J, MINO.I] or
    #         threeMinos == [MINO.I, MINO.T, MINO.J]
    #     ): # IITL
    #         tMove = [MOVE.L_ROT, MOVE.RIGHT] + [MOVE.DOWN for _ in range(alignedBoardTop - FIRST_MINO_POS[1] - 1)] + [MOVE.R_ROT]
    #         iMove = [MOVE.RIGHT, MOVE.DROP]
    #         jMove = [MOVE.R_ROT, MOVE.R_ROT, MOVE.DROP]
    #     elif (
    #         threeMinos == [MINO.J, MINO.I, MINO.T] or 
    #         threeMinos == [MINO.J, MINO.T, MINO.I]
    #     ): # IITL
    #         tMove = [MOVE.R_ROT, MOVE.R_ROT, MOVE.LEFT, MOVE.DROP]
    #         iMove = [MOVE.R_ROT, MOVE.DROP] #FIXME
    #         jMove = [MOVE.L_ROT, MOVE.RIGHT] + [MOVE.DOWN for _ in range(alignedBoardTop - FIRST_MINO_POS[1] - 1)] + [MOVE.LEFT]

    #     # # ITJS
    #     # elif (
    #     #     threeMinos == [MINO.T, MINO.L, MINO.S] or 
    #     #     threeMinos == [MINO.T, MINO.S, MINO.L]
    #     # ): # ITJS
    #     #     tMove = [MOVE.R_ROT] + [MOVE.DOWN for _ in range(alignedBoardTop - FIRST_MINO_POS[1] - 1)] + [MOVE.L_ROT]
    #     #     jMove = [MOVE.R_ROT, MOVE.DROP]
    #     #     if threeMinos == [MINO.T, MINO.J, MINO.S]:
    #     #         sMove = [MOVE.R_ROT, MOVE.RIGHT] + [MOVE.DOWN for _ in range(alignedBoardTop - FIRST_MINO_POS[1] - 1)] + [MOVE.R_ROT] # FIXME
    #     #     else:
    #     #         sMove = [MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
    #     # elif threeMinos == [MINO.J, MINO.S, MINO.T]: # ITJS
    #     #     jMove = [MOVE.R_ROT] + [MOVE.DOWN for _ in range(alignedBoardTop - FIRST_MINO_POS[1] - 1)] + [MOVE.L_ROT]
    #     #     sMove = [MOVE.R_ROT, MOVE.DROP] #FIXME
    #     #     tMove = [MOVE.R_ROT, MOVE.R_ROT, MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]

    #     # # IILZ
    #     # elif (
    #     #     threeMinos == [MINO.Z, MINO.I, MINO.L] or 
    #     #     threeMinos == [MINO.Z, MINO.L, MINO.I] or
    #     #     threeMinos == [MINO.I, MINO.Z, MINO.L]
    #     # ): # IILZ
    #     #     zMove = [MOVE.R_ROT, MOVE.RIGHT] + [MOVE.DOWN for _ in range(alignedBoardTop - FIRST_MINO_POS[1] - 1 - 2)] + [MOVE.L_ROT]
    #     #     iMove = [MOVE.RIGHT, MOVE.DROP]
    #     #     lMove = [MOVE.R_ROT, MOVE.R_ROT, MOVE.RIGHT, MOVE.DROP]

    #     # # IJSZ
    #     # elif (
    #     #     threeMinos == [MINO.Z, MINO.J, MINO.S] or 
    #     #     threeMinos == [MINO.Z, MINO.S, MINO.J]
    #     # ):
    #     #     zMove = [MOVE.R_ROT, MOVE.RIGHT] + [MOVE.DOWN for _ in range(alignedBoardTop - FIRST_MINO_POS[1] - 1 - 2)] + [MOVE.L_ROT]
    #     #     sMove = [MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
    #     #     jMove = [MOVE.R_ROT, MOVE.DROP]
    #     # elif (
    #     #     threeMinos == [MINO.J, MINO.Z, MINO.S]
    #     # ):
    #     #     jMove = [MOVE.RIGHT, MOVE.DROP]
    #     #     zMove = [MOVE.R_ROT, MOVE.DROP]
    #     #     sMove = [MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]

    #     # # IITO
    #     # elif (
    #     #     threeMinos == [MINO.I, MINO.T, MINO.O] or 
    #     #     threeMinos == [MINO.T, MINO.I, MINO.O] or 
    #     #     threeMinos == [MINO.T, MINO.O, MINO.I]
    #     # ):
    #     #     tMove = [MOVE.R_ROT, MOVE.DROP]
    #     #     iMove = [MOVE.RIGHT, MOVE.DROP]
    #     #     oMove = [MOVE.RIGHT, MOVE.DROP]
            
    #     # # IIOJ
    #     # elif (
    #     #     threeMinos == [MINO.I, MINO.O, MINO.J] or 
    #     #     threeMinos == [MINO.O, MINO.I, MINO.J] or 
    #     #     threeMinos == [MINO.O, MINO.J, MINO.I]
    #     # ):
    #     #     iMove = [MOVE.RIGHT, MOVE.DROP]
    #     #     oMove = [MOVE.DROP]
    #     #     jMove = [MOVE.R_ROT, MOVE.R_ROT, MOVE.RIGHT, MOVE.DROP]
            
    #     # # IIJS
    #     # elif (
    #     #     threeMinos == [MINO.I, MINO.S, MINO.J] or 
    #     #     threeMinos == [MINO.S, MINO.I, MINO.J] or 
    #     #     threeMinos == [MINO.S, MINO.J, MINO.I]
    #     # ):
    #     #     iMove = [MOVE.RIGHT, MOVE.DROP]
    #     #     sMove = [MOVE.RIGHT, MOVE.DROP]
    #     #     jMove = [MOVE.RIGHT, MOVE.DROP]
            
    #     # # IITS
    #     # elif (
    #     #     threeMinos == [MINO.I, MINO.T, MINO.S] or 
    #     #     threeMinos == [MINO.T, MINO.I, MINO.S]
    #     # ):
    #     #     iMove = [MOVE.L_ROT, MOVE.DROP]
    #     #     tMove = [MOVE.R_ROT, MOVE.RIGHT, MOVE.DROP]
    #     #     sMove = [MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
            
    #     # # ITLJ
    #     # elif (
    #     #     threeMinos == [MINO.T, MINO.J, MINO.L] or 
    #     #     threeMinos == [MINO.T, MINO.L, MINO.J]
    #     # ):
    #     #     tMove = [MOVE.R_ROT, MOVE.DROP]
    #     #     lMove = [MOVE.L_ROT, MOVE.RIGHT, MOVE.DROP]
    #     #     jMove = [MOVE.L_ROT, MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
            
    #     # # ITSZ
    #     # elif (
    #     #     threeMinos == [MINO.T, MINO.S, MINO.Z] or
    #     #     threeMinos == [MINO.T, MINO.S, MINO.Z]
    #     # ):
    #     #     tMove = [MOVE.R_ROT, MOVE.DROP]
    #     #     sMove = [MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]
    #     #     zMove = [MOVE.RIGHT, MOVE.DROP]

    #     # # IOJT
    #     # elif (
    #     #     threeMinos == [MINO.O, MINO.J, MINO.T]
    #     # ):
    #     #     oMove = [MOVE.DROP]
    #     #     jMove = [MOVE.RIGHT, MOVE.DROP]
    #     #     tMove = [MOVE.R_ROT, MOVE.R_ROT, MOVE.RIGHT, MOVE.RIGHT, MOVE.DROP]

    #     # else
    #     else:
    #         pcState = PCState.Wait
    #         pcReturnValueQueue = []
    #         return []
        
    #     # return
    #     pcReturnValueQueue = AssignPCMinoMoves(
    #         threeMinos,
    #         tMove, oMove, zMove, iMove, lMove, sMove, jMove
    #     )
    #     return [pcReturnValueQueue.pop(0)]

    else:
        # あきらめて帰る
        pcState = PCState.Wait
        pcReturnValueQueue = []
        return []


def SearchPCSecondMove(board:Board, minoNum:int) -> List[List[MoveInt]]:

    # boardsは(盤面、それに至るミノの動き)のリスト
    boards = [(board, [])]
    for _ in range(minoNum):
        nextBoards = []
        for board, accumPath in boards:
            moves = decisionMaker.GetNextMoves(board)

            for mino, path in moves:

                # ラインの消去
                joindBoard, joinedTopRowIdx = JoinDirectedMinoToBoard(mino, board.mainBoard, board.topRowIdx)
                newMainBoard, newTopRowIdx, _ = ClearLines(joindBoard, joinedTopRowIdx)

                # boardAfterHoldは
                # もしHoldをしていたらその操作だけ行った後の盤面
                # そうではないときは元の盤面
                boardAfterHold = board
                if path[0] is MOVE.HOLD:
                    boardAfterHold = BoardAfterHold(board)

                nextBoard = Board(
                    newMainBoard,
                    DirectedMino(
                        boardAfterHold.followingMinos[0],
                        FIRST_MINO_DIRECTION,
                        FIRST_MINO_POS
                    ),
                    boardAfterHold.followingMinos[1:] + [MINO.NONE],
                    boardAfterHold.holdMino,
                    True,
                    newTopRowIdx,
                    boardAfterHold.score,
                    boardAfterHold.backToBack,
                    boardAfterHold.ren,
                    boardAfterHold.minoBagContents
                )

                if BOARD_HEIGHT - min(nextBoard.topRowIdx) <= 4:
                    nextBoards.append((nextBoard, accumPath + [path]))
        
       
            boards = nextBoards

    if boards:
        for board, path in boards:
            if BOARD_HEIGHT - min(board.topRowIdx) == 0:
                return path
        return []              
    else:
        return [] 



# https://harddrop.com/wiki/Perfect_Clear_Opener
# https://tannsokumegane.com/tetris-perfectclear/
# https://tetrisopener.wicurio.com/index.php?%E9%96%8B%E5%B9%95%E3%83%91%E3%83%95%E3%82%A7%E7%A9%8D%E3%81%BF

