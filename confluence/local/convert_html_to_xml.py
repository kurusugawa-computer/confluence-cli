from __future__ import annotations

import argparse
import logging
from pathlib import Path

import pyquery
from lxml.html import HtmlElement, fromstring

import confluence
import confluence.common.cli

logger = logging.getLogger(__name__)


def convert_img_elm(img_elm: HtmlElement) -> None:
    """
    `<img src="foo.png">`を以下のXMLに変換する

    ```
    <ac:image>
    <ri:attachment ri:filename="foo.png"/>
    </ac:image>
    ```

    Args:
        trim_dirname_for_src_value: src属性値からディレクトリ名を削除する。Confluenceにアップロードしたファイル名にスラッシュは含められないため。
    """
    img_elm.tag = "ac:image"
    src_value: str = img_elm.attrib.get("src")
    if src_value.startswith(("http:", "https:")):
        url_elm = fromstring("<ri:url/>")
        # コロン付きのタグが生成できないので、tagを改めて置換する
        url_elm.tag = "ri:url"
        url_elm.attrib["ri:value"] = src_value
        img_elm.append(url_elm)
    else:
        attachment_elm = fromstring("<ri:attachment/>")
        # コロン付きのタグが生成できないので、改めて置換した
        attachment_elm.tag = "ri:attachment"
        # src属性値にスラッシュが含まれていたら、ディレクトリ名を取り除いてファイル名だけを設定する
        # Confluenceにアップロードしたファイルは、ファイル名スラッシュは含められないため、
        tmp = src_value.split("/")
        attachment_elm.attrib["ri:filename"] = tmp[-1]

        img_elm.append(attachment_elm)
    del img_elm.attrib["src"]

    # img要素のいくつかの属性を、`ac:image`タグの属性に変換する。
    # https://ja.confluence.atlassian.com/doc/confluence-storage-format-790796544.html
    # bool値を指定する以下の属性は変換しない
    # ac:border, ac:thumbnail
    for html_attribute_name in ("align", "class", "title", "style", "alt", "height", "width", "vspace", "hspace"):
        attribute_value = img_elm.attrib.get(html_attribute_name)
        print(html_attribute_name, attribute_value)
        if attribute_value is not None and attribute_value != "":
            img_elm.attrib[f"ac:{html_attribute_name}"] = attribute_value
            del img_elm.attrib[html_attribute_name]

    # サムネイル画像として設定する（画像をクリックすると拡大表示される）
    img_elm.attrib["ac:thumbnail"] = "true"


def convert(input_html_file: Path, output_xml_file: Path) -> None:
    with input_html_file.open(encoding="utf-8") as f:
        file_content = f.read()
    pq_html = pyquery.PyQuery(file_content)

    pq_img = pq_html("img")

    for img_elm in pq_img:
        convert_img_elm(img_elm)

    # body要素があればその中身、なければhtmlファイルの中身をアップロードする
    if len(pq_html("body")) > 0:
        # body要素以下のHTMLを取得する
        html_data = pq_html("body").html()
    else:
        # 要素自身のHTMLを取得する
        html_data = str(pq_html)

    output_xml_file.parent.mkdir(exist_ok=True, parents=True)
    output_xml_file.write_text(html_data, encoding="utf-8")


def main(args: argparse.Namespace) -> None:
    convert(args.input_html, args.output_xml)


def add_arguments_to_parser(parser: argparse.ArgumentParser):  # noqa: ANN201
    parser.add_argument(
        "input_html",
        type=Path,
        help="変換元の入力用HTML",
    )
    parser.add_argument(
        "output_xml",
        type=Path,
        help="変換先の出力用XML",
    )

    parser.set_defaults(subcommand_func=main)


def add_parser(subparsers: argparse._SubParsersAction | None = None) -> argparse.ArgumentParser:
    subcommand_name = "convert_html"
    subcommand_help = "HTMLをConfluence用のXMLに変換します。"

    parser = confluence.common.cli.add_parser(subparsers, subcommand_name, subcommand_help)

    add_arguments_to_parser(parser)
    return parser
