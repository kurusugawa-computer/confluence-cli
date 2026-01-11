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



``--representation`` によるフォーマットの指定
==================================================================

各 representation の説明は、以下のドキュメントの説明を引用しています。
https://docs.atlassian.com/atlassian-confluence/6.6.0/com/atlassian/confluence/api/model/content/ContentRepresentation.html


storage （デフォルト）
----------------------------


    Raw database format, for content that stores data in our XML storage format

.. code-block::
    
   <div>
     <h1>テスト</h1>
     <p>サンプル画像</p>
     <p>
       <ac:image ac:thumbnail="true" ac:width="32">
         <ri:attachment ri:filename="A.png"></ri:attachment>
       </ac:image>
     </p>
   </div>


view
----------------------------

    HTML representation for viewing in a web page

.. code-block::
    
   <div>
     <h1 id="id-テスト-テスト">テスト</h1>
     <p>サンプル画像</p>
     <p>
       <span class="confluence-embedded-file-wrapper confluence-embedded-manual-size">
         <img class="confluence-embedded-image confluence-thumbnail" width="32" src="/confluence/download/thumbnails/713424927/A.png?version=1&amp;modificationDate=1768131619959&amp;api=v2" data-image-src="/confluence/download/attachments/713424927/A.png?version=1&amp;modificationDate=1768131619959&amp;api=v2" data-unresolved-comment-count="0" data-linked-resource-id="1735327999" data-linked-resource-version="1" data-linked-resource-type="attachment" data-linked-resource-default-alias="A.png" data-base-url="https://kurusugawa.jp/confluence" data-linked-resource-content-type="image/png" data-linked-resource-container-id="713424927" data-linked-resource-container-version="40">
       </span>
     </p>
   </div>


editor
----------------------------

    Representation suitable for use in the rich text editor

.. code-block::


   <div>
     <h1>テスト</h1>
     <p>サンプル画像</p>
     <p>
       <img class="confluence-embedded-image confluence-thumbnail" width="32" src="/confluence/download/thumbnails/713424927/A.png?version=1&amp;modificationDate=1768131619959&amp;api=v2" data-image-src="/confluence/download/attachments/713424927/A.png?version=1&amp;modificationDate=1768131619959&amp;api=v2" data-unresolved-comment-count="0" data-linked-resource-id="1735327999" data-linked-resource-version="1" data-linked-resource-type="attachment" data-linked-resource-default-alias="A.png" data-base-url="https://kurusugawa.jp/confluence" data-linked-resource-content-type="image/png" data-linked-resource-container-id="713424927" data-linked-resource-container-version="40" title="Yuuji KAWAMATSU &gt; テスト &gt; A.png" data-location="Yuuji KAWAMATSU &gt; テスト &gt; A.png" data-image-height="18" data-image-width="17">
     </p>
   </div>


export_view
----------------------------


    HTML representation for viewing, but with absolute urls, instead of relative urls in the markup.

.. code-block::


   <div>
     <h1 id="id-テスト-テスト">テスト</h1>
     <p>サンプル画像</p>
     <p>
       <span class="confluence-embedded-file-wrapper confluence-embedded-manual-size">
         <img class="confluence-embedded-image confluence-thumbnail" width="32" src="https://kurusugawa.jp/confluence/download/attachments/embedded-page/~kawamatsu_yuuji/%E3%83%86%E3%82%B9%E3%83%88/A.png?api=v2">
       </span>
     </p>
   </div>


styled_view
----------------------------

    A rendered view that includes inline styles in a

.. code-block::

    <html>
      <head>
        <title>テスト</title>
        <style default-inline-css>
        ...
        </style>
        <base href="https://kurusugawa.jp/confluence">
      </head>
      <body>
        <div id="Content" style="padding: 5px;">
          <h1 id="id-テスト-テスト">テスト</h1>
          <p>サンプル画像</p>
          <p>
            <span class="confluence-embedded-file-wrapper confluence-embedded-manual-size">
              <img class="confluence-embedded-image confluence-thumbnail" width="32" src="/confluence/download/thumbnails/713424927/A.png?version=1&amp;modificationDate=1768131619959&amp;api=v2" data-image-src="/confluence/download/attachments/713424927/A.png?version=1&amp;modificationDate=1768131619959&amp;api=v2" data-unresolved-comment-count="0" data-linked-resource-id="1735327999" data-linked-resource-version="1" data-linked-resource-type="attachment" data-linked-resource-default-alias="A.png" data-base-url="https://kurusugawa.jp/confluence" data-linked-resource-content-type="image/png" data-linked-resource-container-id="713424927" data-linked-resource-container-version="40">
            </span>
          </p>
        </div>
      </body>
    </html>


anonymous_export_view
----------------------------

    HTML representation for viewing, but with absolute urls, instead of relative urls in the markup, and macros are rendered as though it is viewed by an anonymous user.

.. code-block::
    
   <div>
     <h1 id="id-テスト-テスト">テスト</h1>
     <p>サンプル画像</p>
     <p>
       <span class="confluence-embedded-file-wrapper confluence-embedded-manual-size">
         <img class="confluence-embedded-image confluence-thumbnail" width="32" src="https://kurusugawa.jp/confluence/download/attachments/embedded-page/~kawamatsu_yuuji/%E3%83%86%E3%82%B9%E3%83%88/A.png?api=v2">
       </span>
     </p>
   </div>

Usage Details
=================================

.. argparse::
   :ref: confluence.page.get_page_body.add_parser
   :prog: confluence page get_body
   :nosubcommands:
   :nodefaultconst: