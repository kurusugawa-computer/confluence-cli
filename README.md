# confluence-cli
来栖川電算のConfluenceを操作するためのCLIです。

# 認証情報の設定

## 環境変数で指定する
環境変数 `CONFLUENCE_USER_NAME` , `CONFLUENCE_USER_PASSWORD`に認証情報を設定してください。

## コマンドライン引数で指定する。
コマンドライン引数 `--confluence_user_name` , `--confluence_user_password`に認証情報を設定してください。

## 標準入力から指定する
上記の方法で指定がない場合は、標準入力から認証情報を設定することができます。


# Command Reference
### attachment get
添付ファイル情報の取得


### attachment create
添付ファイルの作成


### attachment delete
添付ファイルを削除します。



### local convert_html
HTMLをConfluence用のXMLに変換します。
Google DocsのページをConfluenceに移行するときなどに利用できます。
具体的な手順は以下を参照してください。
https://github.com/kurusugawa-computer/confluence-cli/wiki/Google-Docs%E3%82%92Confluence%E3%81%AB%E7%A7%BB%E8%A1%8C%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95
