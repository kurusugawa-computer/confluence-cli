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

    $ confluence attachment create --content_id ${CONTENT_ID} --dir dir/




Usage Details
=================================

.. argparse::
   :ref: confluence.attachment.create_attachment.add_parser
   :prog: confluence attachment create
   :nosubcommands:
   :nodefaultconst: