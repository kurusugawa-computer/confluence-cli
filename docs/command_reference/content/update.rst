======================================
content update
======================================

Description
=================================
コンテンツを更新します。



Examples
=================================

以下のコマンドは、 ``${CONTENT_ID}`` のコンテンツを ``content.xml`` の内容で更新します。

.. code-block::

    $ confluence content update --content_id ${CONTENT_ID} --xml_file content.xml


以下のコマンドは、コンテンツを更新する際にコメントを残します。

.. code-block::

    $ confluence content update --content_id ${CONTENT_ID} --xml_file content.xml --comment "コンテンツを更新しました"







Usage Details
=================================

.. argparse::
   :ref: confluence.content.update_content.add_parser
   :prog: confluence content update
   :nosubcommands:
   :nodefaultconst:
