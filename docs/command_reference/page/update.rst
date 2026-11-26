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


更新前に対象ページと差分を確認するには、``--dry_run`` を指定します。
``--json`` を組み合わせると、標準出力にJSONを出力します。

.. code-block::

    $ confluence page update --page_id ${PAGE_ID} --xml_file page.xml --dry_run --json

JSONには ``page_id``、``title``、``url``、``version``、``status`` が含まれます。
プレビュー時の ``status`` は ``preview`` で、本文の差分は ``diff`` に入ります。
差分が空の場合は本文に変更がありません。
実行時の ``status`` は更新成功なら ``updated``、確認で取り消した場合は ``cancelled`` です。
``version`` は更新成功時には更新後の版番号、それ以外では取得した時点の版番号です。


Usage Details
=================================

.. argparse::
   :ref: confluence.page.update_page.add_parser
   :prog: confluence page update
   :nosubcommands:
   :nodefaultconst:
