======================================
attachment get
======================================

Description
=================================
添付ファイルを削除します。



Examples
=================================

以下のコマンドは、ページ内の添付ファイルをすべて削除します。

.. code-block::

    $ confluence attachment get --content_id ${CONTENT_ID}



Usage Details
=================================

.. argparse::
   :ref: confluence.attachment.delete_attachment.add_parser
   :prog: confluence attachment delete
   :nosubcommands:
   :nodefaultconst: