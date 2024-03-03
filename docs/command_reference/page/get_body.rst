======================================
body get_body
======================================

Description
=================================
ページの内容を取得します。



Examples
=================================

以下のコマンドは、 ``${CONTENT_ID}`` のページのstorageフォーマットを出力します。

.. code-block::

    $ confluence body get_body --content_id ${CONTENT_ID} > output.xml


.. code-block::

    :caption: output.xml
    <p>test</p>



Usage Details
=================================

.. argparse::
   :ref: confluence.page.get_page_body.add_parser
   :prog: confluence page get_body
   :nosubcommands:
   :nodefaultconst: