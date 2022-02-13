from constants.position import BOARD_WIDTH, BOARD_HEIGHT
from constants.mino import MINO
from colored import fg, attr

COLOR_CODES = {
    MINO.T : fg(5),
    MINO.O : fg(3),
    MINO.Z : fg(1),
    MINO.I : fg(6),
    MINO.L : fg(136),
    MINO.S : fg(2),
    MINO.J : fg(4),
    MINO.JAMA : fg(15),
    MINO.NONE : fg(0),
}

# 盤面の色の情報をもらって、それを色付けしながら出力
def PrintBoardWithColor(boardColor, followingMinos, holdMino, reset=False, elapsedTime=None):
    # リセットがTrueであればボードの高さ分戻る
    if reset:
        print("\033[{}A".format(BOARD_HEIGHT), end="", flush=True)
    
    # 盤面の状況を出力
    for i in range(BOARD_HEIGHT):
        if i == 0: # HOLDミノを表示させる行
            print("{}■{}  ".format(COLOR_CODES[holdMino], attr('reset')), end="", flush=True)
        else:
            print("   ", end="", flush=True)

        row = boardColor[i]
        for j in range(BOARD_WIDTH):
            color = row[j]
            print('{}■{}'.format(COLOR_CODES[color], attr('reset')), end="", flush=True)
        
        if 0 <= i < len(followingMinos): # NEXTミノを表示させる行
            print("  {}■{}".format(COLOR_CODES[followingMinos[i]], attr('reset')), flush=True)
        elif elapsedTime is not None and i == BOARD_HEIGHT - 1: # 最後の行に経過時間を掲載する
            print("  elapsed time for one loop: {}(s)".format(elapsedTime), flush=True)
        else:
            print("", flush=True)

