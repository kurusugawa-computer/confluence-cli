======================================
page get_body
======================================

Description
=================================
ページまたはブログの内容を取得します。



Examples
=================================

以下のコマンドは、 ``${PAGE_ID}`` のページのstorageフォーマットを出力します。

.. code-block::

    $ confluence page get_body --page_id ${PAGE_ID} > output.xml


.. code-block::
    :caption: output.xml

    <p>test</p>
    <p><ac:image ac:thumbnail="true" ac:height="62"><ri:attachment ri:filename="A.png" /></ac:image></p>

デフォルトでは storage フォーマットで出力します。
別のrepresentationで出力するには、 ``--representation`` オプションを使用します。
詳細は https://qiita.com/yuji38kwmt/items/4ec92a024ea23a4bb378 を参照してください。


Usage Details
=================================

.. argparse::
   :ref: confluence.page.get_page_body.add_parser
   :prog: confluence page get_body
   :nosubcommands:
   :nodefaultconst: