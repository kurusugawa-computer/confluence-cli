# confluence-cli
来栖川電算が利用しているConfluence v6.15.7を操作するためのCLIです。


[![Build Status](https://app.travis-ci.com/kurusugawa-computer/confluence-cli.svg?branch=main)](https://app.travis-ci.com/kurusugawa-computer/confluence-cli)
[![PyPI version](https://badge.fury.io/py/kci-confluence-cli.svg)](https://badge.fury.io/py/kci-confluence-cli)
[![Python Versions](https://img.shields.io/pypi/pyversions/kci-confluence-cli.svg)](https://pypi.org/project/kci-confluence-cli/)
[![Documentation Status](https://readthedocs.org/projects/confluence-cli/badge/?version=latest)](https://confluence-cli.readthedocs.io/ja/latest/?badge=latest)

# Requirements
Python 3.9+

# Install

```
$ pip install kci-confluence-cli
```

# 使い方

## 認証情報の指定
以下のいずれかの方法で指定できます。

* 環境変数 `CONFLUENCE_USER_NAME` , `CONFLUENCE_USER_PASSWORD` に指定する
* コマンドライン引数 `--confluence_user_name` , `--confluence_user_password`に指定する

上記の方法で認証情報が指定されない場合は、標準入力から認証情報を入力できます。


## ConfluenceのURLの指定
アクセスするConfluenceのURLを、以下のいずれかの方法で指定できます。

* 環境変数 `CONFLUENCE_BASE_URL`に指定する
* コマンドライン引数 `--confluence_base_url`に指定する

上記の方法で指定されない場合は、標準入力から入力できます。

来栖川電算のConfluneceにアクセスする場合は、`https://kurusugawa.jp/confluence`を指定してください。


# Command Reference
https://confluence-cli.readthedocs.io/ja/latest/command_reference/index.html を参照してください。

