# kci-python-devcontainer
[![Build Status](https://travis-ci.com/kurusugawa-computer/kci-python-devcontainer.svg?branch=master)](https://travis-ci.com/kurusugawa-computer/kci-python-devcontainer)

Pythonプロジェクトのテンプレートとなるリポジトリです。
Pythonで新たに開発する際は、このリポジトリをテンプレートとして利用してください。

## 環境構築
VSCodeのRemote-Containersを使ってください。

## サンプルコマンドの実行

```
vscode@example:/workspaces/kci-python-devcontainer$ poetry run kurusugawa-cli 
Usage: kurusugawa-cli [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  address  住所を出力します。


vscode@example:/workspaces/kci-python-devcontainer$ poetry run kurusugawa-cli address
DEBUG    : 2021-07-15 01:02:05,498 : address.py : kci.command.address : address : 'address' command が実行されました。
愛知県名古屋市中区新栄一丁目29-23 アーバンドエル新栄2階
```

## format && lint
```
vscode@example:/workspaces/kci-python-devcontainer$ make format && make lint
```

## test
```
vscode@example:/workspaces/kci-python-devcontainer$ make test
```


## ドキュメント生成
```
vscode@example:/workspaces/kci-python-devcontainer$ make docs
```




## 社内PyPIにアップロードする手順

1. 事前に以下のコマンドを実行しておき、社内PyPIのURLを設定する。

```   
$ poetry config repositories.kci-upload https://kurusugawa.jp/nexus3/repository/KRS-pypi/
```

2. 以下のコマンドを実行する。user_idとpasswordの入力が求められるので、Confluenceのuser_idとpasswordを入力する。

```
$ poetry publish --repository kci-upload --build
```


---------------------------------


## はまじさんdevcontainerから変えた部分
* makeコマンドのインストール
* poetryのインストール方法を変更
* `PIP_DEFAULT_TIMEOUT=100`の追加
* venv環境に自動的にactivationしないようにした. pythonファイルを実行するときは`poetry run python `を使う。




## できたらいいなー
* formatter, linterの設定を全部pyprojet.tomlに書きたい。ライブラリを使えばできるかもしれないけど、そこまでやるべきか。将来的には実現されそう。
