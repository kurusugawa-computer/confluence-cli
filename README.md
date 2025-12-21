# confluence-cli
来栖川電算が利用しているConfluence v6.15.7を操作するためのCLIです。


[![Build Status](https://app.travis-ci.com/kurusugawa-computer/confluence-cli.svg?branch=main)](https://app.travis-ci.com/kurusugawa-computer/confluence-cli)
[![PyPI version](https://badge.fury.io/py/kci-confluence-cli.svg)](https://badge.fury.io/py/kci-confluence-cli)
[![Python Versions](https://img.shields.io/pypi/pyversions/kci-confluence-cli.svg)](https://pypi.org/project/kci-confluence-cli/)
[![Documentation Status](https://readthedocs.org/projects/confluence-cli/badge/?version=latest)](https://confluence-cli.readthedocs.io/ja/latest/?badge=latest)

# Requirements
Python 3.9+

# Install

```bash
$ pip install kci-confluence-cli
```

# Quick Start

環境変数で認証情報を設定:

```bash
export CONFLUENCE_USER_NAME="your_username"
export CONFLUENCE_USER_PASSWORD="your_password"
export CONFLUENCE_BASE_URL="https://your-domain.com/confluence"
```

ページ本文を取得:

```bash
$ confluence page get_body --content_id 12345
```

# Documentation

詳細な使い方は [ドキュメント](https://confluence-cli.readthedocs.io/ja/latest/) を参照してください。

- [Getting Started](https://confluence-cli.readthedocs.io/ja/latest/user_guide/getting_started.html) - インストール方法と基本的な使い方
- [User Guide](https://confluence-cli.readthedocs.io/ja/latest/user_guide/index.html) - チュートリアルと実践的な使い方
- [Command Reference](https://confluence-cli.readthedocs.io/ja/latest/command_reference/index.html) - 全コマンドのリファレンス

