from lib import *
import evaluator

# minoを今の位置からdirectionを変えずに左右に動かして得られるminoのリストを返す
def GetSideMovedMinos (board:Board, mino:DirectedMino) -> List[Tuple[DirectedMino, List[MOVE]]]:
    sideMovedMinos = []

    # 左に動かしていく
    # 左右移動を一回もしない場合はこちら側に含める（そのためにxに+1している）
    x,y = mino.pos[0] + 1, mino.pos[1]
    count = -1
    while True:
        x -= 1
        count += 1
        newMino = DirectedMino(
            mino.mino,
            mino.direction,
            (x,y)
        )
        occupiedPositions = GetOccupiedPositions(newMino)
        if isValidPlace(board.mainBoard, occupiedPositions):
            sideMovedMinos.append((newMino, [MOVE.LEFT for _ in range(count)]))
        else:
            break
    
    # 右に動かしていく
    x,y = mino.pos[0], mino.pos[1]
    count = 0
    while True:
        x += 1
        count += 1
        newMino = DirectedMino(
            mino.mino,
            mino.direction,
            (x,y)
        )
        occupiedPositions = GetOccupiedPositions(newMino)
        if isValidPlace(board.mainBoard, occupiedPositions):
            sideMovedMinos.append((newMino, [MOVE.RIGHT for _ in range(count)]))
        else:
            break
    
    return sideMovedMinos

# minoを今の位置で1回だけ回転を試みた場合に得られるminoのリストに，回転を全く試みない場合を足して返す
def GetRotatedMinos (board:Board, mino:DirectedMino) -> List[Tuple[DirectedMino, List[MOVE]]]:
    rotatedMinos = []

    # 回転なし
    rotatedMinos.append((mino, []))

    # 左回転
    directedMino = Rotate(mino, MOVE.L_ROT, board.mainBoard)
    if directedMino is not None:
        rotatedMinos.append((directedMino, [MOVE.L_ROT]))
    
    # 右回転
    directedMino = Rotate(mino, MOVE.R_ROT, board.mainBoard)
    if directedMino is not None:
        rotatedMinos.append((directedMino, [MOVE.R_ROT]))
    
    return rotatedMinos

def AddToReachableNodes (encodedNode, path:List[MOVE], reachableNodes:Dict[str, List[MOVE]]) -> None:
    if encodedNode not in reachableNodes: # まだreachableNodesに登録されていないものは，登録する
        reachableNodes[encodedNode] = path
    else:
        # すでに登録されていた場合，pathが今までのものより短ければ登録する
        oldPath = reachableNodes[encodedNode]
        if len(path) < len(oldPath):
            reachableNodes[encodedNode] = path

# MOVE.DROPを使うことにより，pathの簡易化を行う
def SimplifyPath (path:List[MOVE]) -> List[MOVE]:
    # 最後には必ずMOVE.DROPをつける
    # 最後にMOVE.DROPをつけるので，最後の連続するMOVE.DOWNは消去できる
    count = 0
    while count < len(path):
        if path[-(count + 1)] is MOVE.DOWN:
            count += 1
        else:
            break
    simplifiedPath = path[:len(path) - count] + [MOVE.DROP]
    return simplifiedPath
        
# boardとそこに置きたいminoを入力して，
# (ミノがおける場所，そこにたどり着く方法)
# という形式のタプルの配列を返す
def GetPossibleMoves(
    board:Board,
    directedMino:DirectedMino,
) -> List[Tuple[DirectedMino, List[MOVE]]]:

    # 到達できるミノをエンコードしたものと，到達するための経路を結ぶ辞書
    reachableNodes = {
        EncodeDirectedMino(directedMino) : []
    }

    # 4方角の全てのミノを最上部で左右に動かす

    undroppedMinos = []

    # そのままの向き
    sideMovedMinos = GetSideMovedMinos(board, directedMino)
    
    for mino, path in sideMovedMinos:
        reachableNodes[EncodeDirectedMino(mino)] = path
    undroppedMinos += sideMovedMinos
    # 右に1回転したもの
    rightRotatedDirectedMino = Rotate(directedMino, MOVE.R_ROT, board.mainBoard)
    if rightRotatedDirectedMino is not None:
        sideMovedMinos = GetSideMovedMinos(board, rightRotatedDirectedMino)
        for mino, path in sideMovedMinos:
            path.insert(0, MOVE.R_ROT)
            reachableNodes[EncodeDirectedMino(mino)] = path
        undroppedMinos += sideMovedMinos
        # 右に2回転(180回転)したもの
        upsideDownRotatedDirectedMino = Rotate(rightRotatedDirectedMino, MOVE.R_ROT, board.mainBoard)
        if upsideDownRotatedDirectedMino is not None:
            sideMovedMinos = GetSideMovedMinos(board, upsideDownRotatedDirectedMino)
            for mino, path in sideMovedMinos:
                path.insert(0, MOVE.R_ROT)
                path.insert(0, MOVE.R_ROT)
                reachableNodes[EncodeDirectedMino(mino)] = path
            undroppedMinos += sideMovedMinos
    # 左に1回転したもの
    leftRotatedDirectedMino = Rotate(directedMino, MOVE.L_ROT, board.mainBoard)
    if leftRotatedDirectedMino is not None:
        sideMovedMinos = GetSideMovedMinos(board, leftRotatedDirectedMino)
        for mino, path in sideMovedMinos:
            path.insert(0, MOVE.L_ROT)
            reachableNodes[EncodeDirectedMino(mino)] = path
        undroppedMinos += sideMovedMinos
    
    # ミノを全て下に落とす

    for mino, path in undroppedMinos:
        dropCount = Drop(board.mainBoard, mino)
        mino.pos = (mino.pos[0], mino.pos[1] + dropCount)
        path += [MOVE.DOWN for _ in range(dropCount)]
        reachableNodes[EncodeDirectedMino(mino)] = path
    droppedMinos = undroppedMinos # リネーム

    # 回転できるところまで回転する

    for mino, path in droppedMinos:
        rightRotatedMino = mino
        leftRotatedMino = mino
        hasRightRotateEnded = False
        hasLeftRotateEnded = False
        rightRotateCount = 1
        leftRotateCount = 1
        while True:
            # 回転数が少なくなるように、R_ROT, L_ROTを交互に実行する
            if not hasRightRotateEnded:
                rightRotatedMino = Rotate(rightRotatedMino, MOVE.R_ROT, board.mainBoard)
                if rightRotatedMino is not None and EncodeDirectedMino(rightRotatedMino) not in reachableNodes: # 回転可能かつまだ到達してない部分
                    reachableNodes[EncodeDirectedMino(rightRotatedMino)] = path + [MOVE.R_ROT for _ in range(rightRotateCount)]
                    rightRotateCount += 1
                else:
                    hasRightRotateEnded = True
            
            if not hasLeftRotateEnded:
                leftRotatedMino = Rotate(leftRotatedMino, MOVE.L_ROT, board.mainBoard)
                if leftRotatedMino is not None and EncodeDirectedMino(leftRotatedMino) not in reachableNodes: # 回転可能かつまだ到達してない部分
                    reachableNodes[EncodeDirectedMino(leftRotatedMino)] = path + [MOVE.L_ROT for _ in range(leftRotateCount)]
                    leftRotateCount += 1
                else:
                    hasLeftRotateEnded = True
            
            # どちらの方向にも回転できなくなったら終了
            if hasRightRotateEnded and hasLeftRotateEnded:
                break

    # 結果出力
    possibleMoves = []
    # 方向は異なるが占領する場所は同じになるミノが存在するので，これらを重複して数えないために利用する
    # 例えばzミノはNとSで位置をずらせば同じ場所を占領するようになる
    encodedPlacesList = set()
    for key in reachableNodes:
        path = SimplifyPath(reachableNodes[key])
        decodedMino = DecodeDirectedMino(key)
        encodedPlaces = EncodePlacesOccupiedByDirectedMino(decodedMino)
        if encodedPlaces in encodedPlacesList:
            # possibleMovesの中から同じ位置を占領することになるdirectedMinoを探索
            sameMino, samePath = None, None
            for mino, path in possibleMoves:
                if (
                    EncodePlacesOccupiedByDirectedMino(mino) == encodedPlaces
                ):
                    sameMino, samePath = mino, path
                    break
            # 今回考えているpathの方が短かったら入れ替え
            possibleMoves.remove((sameMino, samePath))
            possibleMoves.append((decodedMino, path))
        else:
            if CanPut(board.mainBoard, GetOccupiedPositions(decodedMino)): # 空中に浮いたりしていないことをチェック
                possibleMoves.append((
                    decodedMino,
                    path
                ))
                encodedPlacesList.add(encodedPlaces)
    
    return possibleMoves

def Search (board:Board, mino:DirectedMino, path:List[MOVE], limit:int) -> int:
    # 最後のみ盤面自体の評価を行う
    if limit == 0:
        # ライン消去
        joinedMainBoard = JoinDirectedMinoToBoard(mino, board.mainBoard)
        newMainBoard, clearedRowCount = ClearLines(joinedMainBoard)
        return evaluator.EvalPath(path, clearedRowCount, joinedMainBoard, mino) + evaluator.EvalMainBoard(newMainBoard)
    
    # ライン消去
    joinedMainBoard = JoinDirectedMinoToBoard(mino, board.mainBoard)
    newMainBoard, clearedRowCount = ClearLines(joinedMainBoard)
    clearedBoard = Board(
        newMainBoard,
        DirectedMino(
            board.followingMinos[0],
            FIRST_MINO_DIRECTION,
            FIRST_MINO_POS
        ),
        board.followingMinos[1:] + [MINO.NONE],
        board.holdMino,
        True
    )

    possibleMoves = GetPossibleMoves(
        clearedBoard,
        clearedBoard.currentMino
    )

    maxValue = -10000000000
    for possibleMoveMino, possibleMovePath in possibleMoves:
        value = Search(clearedBoard, possibleMoveMino, possibleMovePath, limit-1)
        if value >= maxValue:
            maxValue = value

    return maxValue + evaluator.EvalPath(path, clearedRowCount, joinedMainBoard, mino)

# 実際に手を決める関数
def Decide (board:Board) -> Tuple[DirectedMino, List[MOVE]]:
    possibleMoves = GetPossibleMoves(
        board,
        board.currentMino
    )

    # 評価値計算
    maxValue, maxMino, maxPath = -10000000000, None, None
    threads = []

    with ThreadPoolExecutor() as executor:
        for mino, path in possibleMoves:
            threads.append(executor.submit(Search, board, mino, path, 2-1))
        
        for i in range(len(threads)):
            mino, path = possibleMoves[i]
            thread = threads[i]
            value = thread.result()
            if value >= maxValue:
                maxMino, maxPath = mino, path
                maxValue = value
    
    return maxValue, maxMino, maxPath
