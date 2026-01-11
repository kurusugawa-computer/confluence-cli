======================================
page update
======================================

Description
=================================
ページを更新します。



Examples
=================================

以下のコマンドは、 ``${PAGE_ID}`` のページを ``page.xml`` の内容で更新します。

.. code-block::

    $ confluence page update --page_id ${PAGE_ID} --xml_file page.xml


以下のコマンドは、ページを更新する際にコメントを残します。

.. code-block::

    $ confluence page update --page_id ${PAGE_ID} --xml_file page.xml --comment "ページを更新しました"







Usage Details
=================================

.. argparse::
   :ref: confluence.page.update_page.add_parser
   :prog: confluence page update
   :nosubcommands:
   :nodefaultconst:
