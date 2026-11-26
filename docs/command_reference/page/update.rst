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


取得時点の版番号を指定すると、ページがその後に変更されていた場合に更新を中止できます。
``content get_by_id --content_id ${PAGE_ID} --expand body.storage version`` で取得した
``version.number`` を指定します。

.. code-block::

    $ confluence page update --page_id ${PAGE_ID} --xml_file page.xml --expected_version 7 --yes


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
