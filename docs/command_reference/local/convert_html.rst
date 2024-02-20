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


.. code-block::

    :caption: input.xml

    <html>
    <body>
    <img alt="" src="foo.png" title="foo-title" alt="foo-alt">
    <img alt="" src="https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png">
    </body>
    </html>


.. code-block::
    :caption: output.xml


    <ac:image alt="" src="foo.png" title="foo-title" ac:thumbnail="true" ac:title="foo-title">
        <ri:attachment ri:filename="foo.png" />
    </ac:image>
    <ac:image alt="" src="https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
        ac:thumbnail="true" ac:title="">
        <ri:url ri:value="https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png" />
    </ac:image>


source editorにXMLを入力する前に、 ``<ri:attachment ri:filename="foo.png" />`` で参照されているファイルを添付ファイルとして作成する必要があります。






Usage Details
=================================

.. argparse::
   :ref: confluence.local.convert_html_to_xml.add_parser
   :prog: confluence local convert_html
   :nosubcommands:
   :nodefaultconst: