======================================
attachment create
======================================

Description
=================================
添付ファイルを作成します。



Examples
=================================

以下のコマンドは、``dir`` ディレクトリ配下のファイルをConfluenceにアップロードして、添付ファイルを作成します。

.. code-block::

    $ confluence attachment create --parent_content_id ${CONTENT_ID} --dir dir/



アップロード先にすでに同じファイルが存在している場合は400 Errorが発生します。アップロード先のファイルを上書きする場合は、 ``--allow_duplicated`` を指定してください。

.. code-block::

    $ confluence attachment create --parent_content_id ${CONTENT_ID} \
     --file file1.txt file2.txt --allow_duplicated





Usage Details
=================================

.. argparse::
   :ref: confluence.attachment.create_attachment.add_parser
   :prog: confluence attachment create
   :nosubcommands:
   :nodefaultconst: