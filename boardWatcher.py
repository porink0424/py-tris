from lib import *

# 指定した1ブロック分の情報を取得する
# 0.005s 程度かかる
def GetPixelColor (pos:Tuple[int], img = None):
    if img is None: # imgが与えられなかったときは自分で作成する
        with mss.mss() as sct:
            posX, posY = GetCenterPosition(pos[1], pos[0])
            region = {'top': WINDOW_Y + posY, 'left': WINDOW_X + posX, 'width': 1, 'height': 1}
            img = sct.grab(region)
            img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
            pixel = img.getpixel((0,0))
    else: # タイミングを合わせたい等でimgが引数として与えられた場合はそれを利用する
        posX, posY = GetCenterPosition(pos[1], pos[0])
        pixel = img.getpixel((posX*2, posY*2))
    
    mino = DetermineColor(pixel[0], pixel[1], pixel[2], pos)
    return mino

# 盤面の状況を配列として返す
# エフェクトの処理方法は以下の通り：
# 1. 1行がお邪魔ブロックからなる行であるかを判定する
# 2. お邪魔ラインである場合、空いている1つがどの列にあるか判定して、認識
# 3. お邪魔ラインでない場合、色ごとに認識する。MINO.JAMAは存在し得ないので、MINO.JAMAと認識された場合は保留しておいて後でもう一度判定を行う
debugf = open("debug.txt", "a")
def GetMainBoard(img):
    # windowのなかのピクセルの色を読み取る
    pixels = []
    for i in range(DISPLAYED_BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            posX, posY = GetCenterPosition(i, j)
            pixels.append(img.getpixel((posX*2, posY*2))) # getpixelのバグ？で2倍しないと正しい部分のrgbをとってくれない
    
    # 盤面の色を判断する
    mainBoard = [0b0 for _ in range(BOARD_HEIGHT - DISPLAYED_BOARD_HEIGHT)]
    laterCheckedPos = [] # お邪魔ラインでないと判定された列であるにもかかわらず、MINO.JAMAと判定された場所を格納していくリスト
    for i in range(DISPLAYED_BOARD_HEIGHT):
        row = 0b0
        # お邪魔ブロックからなるラインであるかどうか判定
        jamaCount = 0
        for j in range(BOARD_WIDTH):
            pixel = pixels[10*i + j]
            if DetermineColor(pixel[0], pixel[1], pixel[2], (i,j)) is MINO.JAMA:
                jamaCount += 1
        if jamaCount >= BOARD_WIDTH - 1: # お邪魔ラインである場合
            for j in range(BOARD_WIDTH):
                pixel = pixels[10*i + j]
                if DetermineColor(pixel[0], pixel[1], pixel[2], (i,j)) is not MINO.JAMA:
                    row |= 0b1111111111 ^ (0b1000000000 >> j)
                    break
        else: # お邪魔ラインでない場合
            for j in range(BOARD_WIDTH):
                pixel = pixels[10*i + j]
                if DetermineColor(pixel[0], pixel[1], pixel[2], (i,j)) is MINO.JAMA: # 邪魔ブロックがあることはあり得ないため、エフェクトと重なっていると考えられる。今は保留して、後にもう一度判定を行う
                    laterCheckedPos.append((j,i))
                elif DetermineColor(pixel[0], pixel[1], pixel[2], (i,j)) is not MINO.NONE:
                    row |= 0b1000000000 >> j
        mainBoard.append(row)

    # 保留されていた部分をもう一度判定する
    while laterCheckedPos:
        pos = laterCheckedPos.pop()
        mino = GetPixelColor((pos[0], pos[1]))
        if mino is MINO.JAMA:
            laterCheckedPos.insert(0, pos)
        elif mino is not MINO.NONE:
            mainBoard[pos[1] + (BOARD_HEIGHT - DISPLAYED_BOARD_HEIGHT)] |= 0b1000000000 >> pos[0]
    
    debugf.write("\n".join(map(str, mainBoard)))
    debugf.write("\n\n\n\n")
    
    return mainBoard

# 現在のミノを取得
# FIRST_MINO_POSの位置から現在のミノの情報を取得することを試みる。そこで見つかれなければ、見る場所を真下に移していく。
# 見つかったらその周りのブロックも見て、中心位置を割り出し、DirectedMinoを返す
def GetCurrentMino(img = None) -> DirectedMino:
    # ミノの種類を割り出す
    pos = (FIRST_MINO_POS[0], FIRST_MINO_POS[1] - (BOARD_HEIGHT - DISPLAYED_BOARD_HEIGHT))
    while True:
        mino = GetPixelColor(pos, img)
        if mino is not MINO.NONE and mino is not MINO.JAMA:
            break
        pos = (pos[0], pos[1]+1)
        if pos[1]+1 > DISPLAYED_BOARD_HEIGHT:
            pos = (FIRST_MINO_POS[0], FIRST_MINO_POS[1] - (BOARD_HEIGHT - DISPLAYED_BOARD_HEIGHT))
    
    # 中心位置を割り出す（T,S,Z,Oについて、中心位置がposとずれていないか確認する必要がある）
    if mino in {MINO.T, MINO.S, MINO.Z, MINO.O}:
        if GetPixelColor((pos[0], pos[1]+1), img) is not mino:
            pass
        else:
            pos = (pos[0], pos[1]+1)
    
    return DirectedMino(
        mino,
        DIRECTION.N,
        (pos[0], pos[1] + (BOARD_HEIGHT - DISPLAYED_BOARD_HEIGHT))
    )
    

# NEXT以降のミノを配列として返す（仮の実装。todo: もうちょい上手い方法はないか）
def GetFollowingMinos(img):
    followingMinos = []

    for yRange in NEXT_MINOS_Y_RANGES:
        # ちゃんと候補が見つかるまでposXを変えながら実行する
        posX = NEXT_MINOS_X
        while True:
            candidates = [] # 判断の結果を一時的に保存する配列を用意
            for posY in range(yRange[0], yRange[1]):
                r,g,b = img.getpixel((posX*2, posY*2))
                color = DetermineColor(r,g,b, (posX,posY))

                # ピクセルごとに見ているので、同じミノであると連続的に判定されることになる
                # その連続は1つのミノを見ているとみなす
                if (
                    color is not MINO.NONE and # 空白でもない
                    color is not MINO.JAMA and # お邪魔部分でもない
                    (len(candidates) == 0 or candidates[-1] is not color) # いままで登録されていなかった色だった場合
                ):
                    candidates.append(color)
            
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
            r,g,b = img.getpixel((posX*2, posY*2))
            color = DetermineColor(r,g,b, (posX,posY))
        
            # ピクセルごとに見ているので、同じミノであると連続的に判定されることになる
            # その連続は1つのミノを見ているとみなす
            if (
                color is not MINO.NONE and # 空白でもない
                color is not MINO.JAMA and # お邪魔部分でもない
                (len(candidates) == 0 or candidates[-1] is not color) # いままで登録されていなかった色だった場合
            ):
                candidates.append(color)
        
        # 正常時に判定できているときはcandidatesにはただ1つ要素が入るはず
        if (len(candidates) == 1):
            return candidates[0]
        # 1つに絞れなかったのでposXを変えて再度判断
        else:
            posX -= 2
            if posX < HOLD_MINO_BOX_X: # ホールドボックスのサイズを超えてしまっている
                return MINO.NONE
    