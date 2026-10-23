# confluence-cli
Confluence v6.15.7を操作するためのCLIです。


[![Test](https://github.com/kurusugawa-computer/confluence-cli/actions/workflows/lint-test.yml/badge.svg)](https://github.com/kurusugawa-computer/confluence-cli/actions/workflows/lint-test.yml)
[![PyPI version](https://badge.fury.io/py/kci-confluence-cli.svg)](https://badge.fury.io/py/kci-confluence-cli)
[![Python Versions](https://img.shields.io/pypi/pyversions/kci-confluence-cli.svg)](https://pypi.org/project/kci-confluence-cli/)
[![Documentation Status](https://readthedocs.org/projects/confluence-cli/badge/?version=latest)](https://confluence-cli.readthedocs.io/ja/latest/?badge=latest)

# Requirements
Python 3.12+

# Install

```bash
$ pip install kci-confluence-cli
```

`uv` を使用している場合は、インストールせずに実行することもできます。

```bash
$ uvx --from kci-confluence-cli confluence page get_body --page_id 123456
```

Python clientとして利用する場合は、共通のtimeout、redirect、response size policyを指定できます。

```python
from confluence.common.api import Api, TransportPolicy

api = Api(
    username,
    password,
    base_url,
    transport_policy=TransportPolicy(
        timeout_second=10,
        follow_redirects=False,
        response_byte_bound=2 * 1024 * 1024,
    ),
)
content = api.get_content_by_id(content_id, query_params={"expand": "space,body.storage,version,ancestors"})
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
$ confluence page get_body --page_id 123456
```

# Documentation

詳細な使い方は [ドキュメント](https://confluence-cli.readthedocs.io/ja/latest/) を参照してください。

- [Getting Started](https://confluence-cli.readthedocs.io/ja/latest/user_guide/getting_started.html) - インストール方法と基本的な使い方
- [User Guide](https://confluence-cli.readthedocs.io/ja/latest/user_guide/index.html) - チュートリアルと実践的な使い方
- [Command Reference](https://confluence-cli.readthedocs.io/ja/latest/command_reference/index.html) - 全コマンドのリファレンス

## シークレット検査

`make gitleaks` で現在のブランチの Git 履歴を検査します。gitleaks をインストール済みならそのコマンドを使い、未インストールなら Docker で v8.30.1 を実行します。検出値はログでマスクします。CI でも同じ検査を実行します。

コミット前の差分検査には pre-commit フックを利用できます。

```sh
uv sync --locked
uv run pre-commit install
```

Docker の接続先・認証設定は、通常利用している設定を引き継ぎます。設定ディレクトリを明示的に切り替える場合のみ、`GITLEAKS_DOCKER_CONFIG=/tmp/gitleaks-docker-config make gitleaks` のように指定してください。
