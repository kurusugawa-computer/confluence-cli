======================================
content get_by_id
======================================

Description
=================================
コンテンツの情報を取得します。



Examples
=================================

以下のコマンドは、 ``${CONTENT_ID}`` のコンテンツ情報を取得します。

.. code-block::

    $ confluence content get_by_id --content_id ${CONTENT_ID} > output.json


.. code-block::

    :caption: output.json

    {
        "id": "863699179",
        "type": "page",
        "status": "current",
        "title": "test",
        "space": {
        "id": 690323457,
        "key": "parent",
        "name": "yuji38kwmt",
        "type": "personal",
        "_links": {},
        ...
    }







Usage Details
=================================

.. argparse::
   :ref: confluence.content.get_content_by_id.add_parser
   :prog: confluence content get_by_id
   :nosubcommands:
   :nodefaultconst: