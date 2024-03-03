# confluence-cli
来栖川電算が利用しているConfluence v6.15.7を操作するためのCLIです。

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
### attachment get
添付ファイル情報の取得


### attachment create
添付ファイルの作成


### attachment delete
添付ファイルを削除します。

※添付ファイルをゴミ箱から完全に削除すると、ページを更新できない場合があります。その場合は、一時的に前のバージョンに戻せば、ページを更新できるようになります。
https://qiita.com/yuji38kwmt/items/c88f039e02b8508926e6


### attachment get
コンテンツ（ページやブログ、添付ファイルなど）の情報を取得します。

### local convert_html
HTMLをConfluence用のXMLに変換します。
Google DocsのページをConfluenceに移行するときなどに利用できます。
具体的な手順は以下を参照してください。
https://github.com/kurusugawa-computer/confluence-cli/wiki/Google-Docs%E3%82%92Confluence%E3%81%AB%E7%A7%BB%E8%A1%8C%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95
