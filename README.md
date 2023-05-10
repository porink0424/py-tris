# py-tris

ぷよテトのテトリスAIをつくるプロジェクト


## Pre-Requests

プログラムの実行環境

```
Python3 3.9.1
```

実行に必要なpythonのモジュール

```
PyAutoGUI==0.9.53
mss==6.1.0
Pillow==8.1.0
colored==1.4.3
cython=0.29.28
Pymem==1.8.5
vgamepad==0.0.7
pywin32==303
```

GUIの実行に必要なパッケージ

```
yarn 1.22.17
```

実行対象

```
Windows10
PuyoPuyo Tetris (in Steam)
```



## Usage

### パッケージ化

```
yarn

yarn run make
```

### コンパイル

```
python setup.py build_ext --inplace
```

### コマンドラインからの実行

- simulatorでの実行を見たい場合

```
python main.py sim
```

- アプリケーション上で実行したい場合

```
python main.py app
```

### 注意点

開発時は、コンパイルせずにそのまま実行する方がデバッグがしやすい。コンパイルで出たファイルを消したい時は、rm.shを実行すればよい：

```
sh rm.sh
```

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
