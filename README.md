# 対話型音声合成最適化

## 概要

このCLIアプリでは、対話型進化計算を用いた対話型音声合成最適化プロセスを体験できます。
対話型進化計算では、ユーザーからの評価を逐次入力することで最適化を進めていきます。
そのため、各ユーザーの嗜好に合った最適化を実現できます。

このアプリでは音声合成の最適化を題材として、対話型進化計算による最適化プロセスを構築してあります。
5つの元となる音声が用意されており、それら音声の合成具合（どの合成された音声がユーザーにとって好みか）を評価することで最適化を行います。
したがって、最終的にユーザーは自身の嗜好に最も合った解（音声）を得ることができます。

## セットアップ方法

### 前提条件

本アプリは以下の環境が準備されていることを前提とする。

* makeファイルの実行環境
* docker/docker composeの実行環境

### 手順

1. ローカル環境へリポジトリを`git clone`する。
   ```
   $ git clone https://github.com/yu-chap/SoundOptimization.git
   ```
2. `make setup`コマンドを実行し、環境構築を行う。
   ```
    $ make setup
   ```
3. `make ps`コマンドを実行し、コンテナが立ち上がっていることを確認する。
   ```
   $ make ps
    NAME                      COMMAND             SERVICE             STATUS              PORTS
    soundoptimization-app-1   "python3"           app                 running
   ```

## アプリ実行方法

### 前準備

コンテナが立ち上がっていない場合、以下のコマンドでコンテナを立ち上げる。

```
$ make up
```

すでにアプリを実行済みであった場合、以下のコマンドで最適化データを初期化する。
（前回のアプリ実行時に生成されたファイルを削除する。）

```
$ make fresh
```

### 最適化プロセス

1. `make start`コマンドを実行し、アプリを実行する。
   ```
   $ make start
   ```
2. ターミナルで以下の表示が出力されるため、`1`を入力（もし、最適化を終了する場合は`0`を入力）する。
   ```
   Please input 1 to proceed with optimization or 0 to terminate.
   -> 1
   ```
3. 合成された音声が`SoundOptimization/src/data/evaluation/`配下に生成されるため、`parent.wav`と`offspring.wav`
   を聴き、好みの方を以下の入力欄に入力する。（parentの方が好みの場合は`0`、offspringの方が好みの場合は`1`
   を入力する。）この操作を全合成回数（デフォルトでは5回）実行する。
   ```
   Which is better for you, parent or offspring? 0: parent, 1: offspring.
   Please input ->
   ```
4. ステップ2に戻る。

### 最適化終了後

最適化終了後、以下のような文言がターミナルに出力され、最終結果が`SoundOptimization/src/data/result/`配下に保存される。

```
The final result was saved in /app/data/result.
Terminate sound optimization.
```