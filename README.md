# py-tris

## ぷよテトのテトリスAIをつくるプロジェクト

2022/02/13始動

## Pre-Requests

```
Python3
Parallels Desktop & Windows10
PuyoPuyo Tetris (in Steam)
```

### Python Modules Required

- pyautogui
- playsound
- mss
- Pillow
- colored

## Development Rules

### ファイル管理方法について

厳密な決まりは設けていないが，共通で利用する（あるいは今後共通で利用するだろうと思われる）関数やクラスは`lib`に実装すること。`lib`内の分類は大まかに以下の通り：

- `classes` : 共通して使われるクラス
- `constants` : プロジェクト内で使われる定数
- `helpers` : プロジェクト内で使われる関数

### 設計について

基本的には`class.drawio`の簡易的なクラス図に従う。

### commitについて

コミットメッセージについては，何か新しい機能を実装したときは`feat: hogehogehoge`，また，bugフィックスなどの修正を加えたときは`fix: fugafugafuga`の形式とする。

### branch運用について

新機能の実装は`feat/foobar`，修正は`fix/foobar`の形式とする。PRの向きは`master`とする。基本的にブランチは`master`から切るようにすること。 

## Important Points when Verifying in App

- ウィンドウサイズはプログラム起動時から動かしてはいけない
- ウィンドウが他のウィンドウと被ってない
- Parallels Desktopウィンドウ内でプヨテトの画面が全画面表示になっている