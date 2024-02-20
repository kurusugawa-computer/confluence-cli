======================================
attachment get
======================================

Description
=================================
添付ファイルの情報を取得します。



Examples
=================================

以下のコマンドは、ページ内の添付ファイルの情報を出力します。

.. code-block::

    $ confluence attachment get --content_id ${CONTENT_ID} > out.json



.. code-block::

    :caption: out.json


    [
    {
        "id": "1521975743",
        "type": "attachment",
        "status": "current",
        "title": "B",
        "metadata": {
        "mediaType": "image/png",
        "labels": {
            }
        },
        "_expandable": {
            "currentuser": "",
            "properties": "",
            "frontend": "",
            "editorHtml": ""
        }
        },
        "extensions": {
        },
        "_links": {
        },
        "_expandable": {
        }
    }
    ]



Usage Details
=================================

.. argparse::
   :ref: confluence.attachment.get_attachment.add_parser
   :prog: confluence attachment get
   :nosubcommands:
   :nodefaultconst: