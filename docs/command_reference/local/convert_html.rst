======================================
local convert_html
======================================

Description
=================================
HTMLをConfluence用のXMLに変換します。



Examples
=================================

以下のコマンドは、``input.html`` をConfluence用のXML ``output.xml`` に変換します。出力結果のXMLはConfluenceのsource editorに貼り付けることができます。

.. code-block::

    $ confluence local convert_html input.html output.xml


.. code-block:: html
    :caption: input.html

    <html>
    <body>
    <img src="foo.png" title="foo-title" alt="foo-alt">
    <img src="https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png">
    </body>
    </html>


.. code-block:: xml
    :caption: output.xml


    <ac:image ac:title="foo-title" ac:alt="foo-alt" ac:thumbnail="true">
        <ri:attachment ri:filename="foo.png"/>
    </ac:image>
    <ac:image ac:thumbnail="true">
        <ri:url ri:value="https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"/>
    </ac:image>
    

source editorにXMLを入力する前に、 ``<ri:attachment ri:filename="foo.png" />`` で参照されているファイルを添付ファイルとして作成する必要があります。


補足
=================================
Google DocsのページをConfluenceに移行するときの手順を、GitHub Wikiに記載しました。
https://github.com/kurusugawa-computer/confluence-cli/wiki/Google-Docs%E3%82%92Confluence%E3%81%AB%E7%A7%BB%E8%A1%8C%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95



img要素の変換
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``img`` 要素の ``src`` 属性に指定されているディレクトリは無視されます。

.. code-block:: html
    :caption: 変換前のHTML

    <img src="images/bar.png">


.. code-block:: html
    :caption: 変換後のXML

    <ac:image ac:thumbnail="true" >
    <ri:attachment ri:filename="bar.png"/>
    </ac:image>


Data URLが含まれた画像（Base64形式）は、Confluence用のXMLには対応していません。
別の手段で、直接画像を参照する形式に変換してから、 ``local convert_html`` を実行してください。



Usage Details
=================================

.. argparse::
   :ref: confluence.local.convert_html_to_xml.add_parser
   :prog: confluence local convert_html
   :nosubcommands:
   :nodefaultconst: