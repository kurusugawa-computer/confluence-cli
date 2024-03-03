======================================
attachment get
======================================

Description
=================================
添付ファイルを削除します。



Examples
=================================

以下のコマンドは、ページ内の添付ファイルをすべて削除します。削除された添付ファイルはゴミ箱に移動されます。

.. code-block::

    $ confluence attachment delete --content_id ${CONTENT_ID}


``--purge`` を指定すると、ゴミ箱からも削除します。

.. code-block::

    $ confluence attachment delete --content_id ${CONTENT_ID} --purge



補足
=================================
``--purge`` を指定して添付ファイルをゴミ箱から完全に削除すると、ページを更新できない場合があります。その場合は、一時的に前のバージョンに戻せば、ページを更新できるようになります。
https://qiita.com/yuji38kwmt/items/c88f039e02b8508926e6


Usage Details
=================================

.. argparse::
   :ref: confluence.attachment.delete_attachment.add_parser
   :prog: confluence attachment delete
   :nosubcommands:
   :nodefaultconst: