from constants.mino import MINO
from constants.position import BOARD_WIDTH, BOARD_HEIGHT, NEXT_MINOS_X, NEXT_MINOS_Y_RANGES, NEXT_MINOS_BOX_X, HOLD_MINO_X, HOLD_MINO_Y_RANGE, HOLD_MINO_BOX_X
from helpers.position import GetCenterPosition
from helpers.color import DetermineColor

# 盤面の状況を配列として返す
def GetBoardWithColor(img):
    # windowのなかのピクセルの色を読み取る
    pixels = []
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            posX, posY = GetCenterPosition(i, j)
            pixels.append(img.getpixel((posX, posY)))
    
    # 盤面の色を判断する
    board = []
    for i in range(BOARD_HEIGHT):
        row = []
        for j in range(BOARD_WIDTH):
            pixel = pixels[10*i + j]
            mino = DetermineColor(pixel[0], pixel[1], pixel[2], (i,j))
            row.append(mino)
        board.append(row)
    
    return board

# NEXT以降のミノを配列として返す（仮の実装。todo: もうちょい上手い方法はないか）
def GetFollowingMinos(img):
    followingMinos = []

    for yRange in NEXT_MINOS_Y_RANGES:
        # ちゃんと候補が見つかるまでposXを変えながら実行する
        posX = NEXT_MINOS_X
        while True:
            candidates = [] # 判断の結果を一時的に保存する配列を用意
            for posY in range(yRange[0], yRange[1]):
                r,g,b = img.getpixel((posX, posY))
                color = DetermineColor(r,g,b, (posX,posY))

                # ピクセルごとに見ているので、同じミノであると連続的に判定されることになる
                # その連続は1つのミノを見ているとみなす
                if (
                    color is not MINO.NONE and # 空白でもない
                    color is not MINO.JAMA and # お邪魔部分でもない
                    (len(candidates) == 0 or candidates[-1] is not color) # いままで登録されていなかった色だった場合
                ):
                    candidates.append(color)
            
            # ピクセルごとに見ているので、途中で違うミノの色とかぶって誤判定を起こすことがある
            # そのような場合は以下の経験則によりはじく
            if (len(candidates) > 1):
                if (candidates[0] is MINO.J and candidates[1] is MINO.I and candidates[1] is MINO.J):
                    candidates = [candidates[0]]
                elif (candidates[0] is MINO.O and candidates[1] is MINO.L and candidates[1] is MINO.O):
                    candidates = [candidates[0]]
            
            # 正常時に判定できているときはcandidatesにはただ1つ要素が入るはず
            if (len(candidates) == 1):
                followingMinos.append(candidates[0])
                break
            # 1つに絞れなかったのでposXを変えて再度判断
            else:
                posX -= 2
                if posX < NEXT_MINOS_BOX_X: # ネクストボックスのサイズを超えてしまっているので、ゲームが止まっているなどのほかの原因があるはず
                    followingMinos.append(MINO.JAMA)
                    break
    
    return followingMinos

# HOLDのミノを返す（仮の実装。todo: もうちょい上手い方法はないか）
def GetHoldMino(img):
    posX = HOLD_MINO_X
    # ちゃんと候補が見つかるまでposXを変えながら実行する
    while True:
        candidates = [] # 判断の結果を一時的に保存する配列を用意
        for posY in range(HOLD_MINO_Y_RANGE[0], HOLD_MINO_Y_RANGE[1]):
            r,g,b = img.getpixel((posX, posY))
            color = DetermineColor(r,g,b, (posX,posY))
        
            # ピクセルごとに見ているので、同じミノであると連続的に判定されることになる
            # その連続は1つのミノを見ているとみなす
            if (
                color is not MINO.NONE and # 空白でもない
                color is not MINO.JAMA and # お邪魔部分でもない
                (len(candidates) == 0 or candidates[-1] is not color) # いままで登録されていなかった色だった場合
            ):
                candidates.append(color)
            
            # ピクセルごとに見ているので、途中で違うミノの色とかぶって誤判定を起こすことがある
            # そのような場合は以下の経験則によりはじく
            if (len(candidates) > 1):
                if (candidates[0] is MINO.J and candidates[1] is MINO.I and candidates[1] is MINO.J):
                    candidates = [candidates[0]]
                elif (candidates[0] is MINO.O and candidates[1] is MINO.L and candidates[1] is MINO.O):
                    candidates = [candidates[0]]
            
            # 正常時に判定できているときはcandidatesにはただ1つ要素が入るはず
            if (len(candidates) == 1):
                return candidates[0]
            # 1つに絞れなかったのでposXを変えて再度判断
            elif len(candidates) > 1:
                print(*candidates) # debug
            else:
                posX -= 2
                if posX < HOLD_MINO_BOX_X: # ホールドボックスのサイズを超えてしまっているので、ゲームが止まっているなどのほかの原因があるはず
                    return MINO.JAMA
    