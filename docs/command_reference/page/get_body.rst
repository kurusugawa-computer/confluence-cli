======================================
body get_body
======================================

Description
=================================
ページまたはブログの内容を取得します。



Examples
=================================

以下のコマンドは、 ``${CONTENT_ID}`` のページの `storageフォーマット <https://ja.confluence.atlassian.com/doc/confluence-storage-format-790796544.html>`_ を出力します。

.. code-block::

    $ confluence page get_body --content_id ${CONTENT_ID} > output.xml


.. code-block::
    :caption: output.xml

    <p>test</p>
    <p><ac:image ac:thumbnail="true" ac:height="62"><ri:attachment ri:filename="A.png" /></ac:image></p>



Usage Details
=================================

.. argparse::
   :ref: confluence.page.get_page_body.add_parser
   :prog: confluence page get_body
   :nosubcommands:
   :nodefaultconst: