==================================================
Getting Started
==================================================

このページでは、confluence-cliのインストール方法と基本的な使い方を説明します。

Requirements
==================================================

* Python 3.12以上


Install
==================================================


.. code-block:: bash

   $ pip install kci-confluence-cli

``uv`` を使用している場合は、インストールせずに実行することもできます。

.. code-block:: bash

   $ uvx --from kci-confluence-cli confluence page get_body --page_id 123456



Usage
==================================================

認証情報の指定
--------------------------------------------------

Confluenceにアクセスするための認証情報は、以下のいずれかの方法で指定できます。

環境変数で指定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   export CONFLUENCE_USER_NAME="your_username"
   export CONFLUENCE_USER_PASSWORD="your_password"

コマンドライン引数で指定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   $ confluence --confluence_user_name your_username --confluence_user_password your_password [command]

標準入力から指定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

上記の方法で認証情報が指定されない場合は、コマンド実行時に標準入力から認証情報を入力できます。


ConfluenceのURLの指定
--------------------------------------------------

アクセスするConfluenceのURLは、以下のいずれかの方法で指定できます。

環境変数で指定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   export CONFLUENCE_BASE_URL="https://your-domain.com/confluence"

コマンドライン引数で指定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   $ confluence --confluence_base_url https://your-domain.com/confluence [command]

標準入力から指定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

上記の方法で指定されない場合は、コマンド実行時に標準入力からURLを入力できます。


``content_id`` の調べ方
--------------------------------------------------


非対話での実行
==============================

スクリプトなどで実行する場合は、サブコマンドに ``--non_interactive`` を指定します。
認証情報はコマンドライン引数または環境変数で設定します。両方に設定した項目は引数を優先します。
認証情報が不足すると、入力を求めず、エラーメッセージを標準エラー出力に出して終了コード 2 で終了します。

``page update`` で実際にページを更新する場合は、あわせて ``--yes`` を指定します。
確認入力が必要な ``attachment delete`` は非対話モードでは実行できません。
