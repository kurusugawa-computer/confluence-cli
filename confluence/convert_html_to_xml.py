import logging
from argparse import ArgumentParser
from pathlib import Path

import pyquery

logger = logging.getLogger(__name__)


def convert_img_elm(img_elm):
    """
    `<img src="foo.png">`を以下のXMLに変換する

    ```
    <ac:image ac:alt="aaaa" ac:border="true" ac:height="207" ac:title="aaaa" ac:width="240">
    <ri:attachment ri:filename="image2023-2-16_11-24-17.png"/>
    </ac:image>
    ```


    ```
    <ac:image><ri:url ri:value="http://confluence.atlassian.com/images/logo/confluence_48_trans.png" /></ac:image>
    ```
    """
    img_elm.tag = "ac:image"
    src_value: str = img_elm.attrib.get("src")
    if src_value.startswith("http:") or src_value.startswith("https:"):
        url_elm = pyquery.PyQuery("ri:url")
        url_elm.attr("ri:value", src_value)
        img_elm.append(url_elm[0])
    else:
        attachment_elm = pyquery.PyQuery("ri:attachment")
        attachment_elm.attr("ri:filename", src_value)
        img_elm.append(attachment_elm[0])

    img_elm.attrib["ac:thumbnail"] = "true"

    alt_value: str = img_elm.attrib.get("alt")
    if alt_value != "":
        img_elm.attrib["ac:alt"] = alt_value

    title_value: str = img_elm.attrib.get("title")
    if title_value != "":
        img_elm.attrib["ac:title"] = title_value


def convert(input_html_file: Path, output_html_file: Path) -> None:
    with input_html_file.open(encoding="utf-8") as f:
        file_content = f.read()
    pq_html = pyquery.PyQuery(file_content)

    pq_img = pq_html("img")

    # 画像をすべてアップロードして、img要素のsrc属性値を annofab urlに変更する
    for img_elm in pq_img:
        convert_img_elm(img_elm)

        # src_value: str = img_elm.attrib.get("src")
        # if src_value is None:
        #     continue

        # if src_value.startswith("http:") or src_value.startswith("https:"):
        #     continue

        # if src_value.startswith("data:"):
        #     img_path = save_image_from_data_uri_scheme(src_value, temp_dir=temp_dir)
        # else:
        #     if src_value[0] == "/":
        #         img_path = Path(src_value)
        #     else:
        #         img_path = html_path.parent / src_value

    # body要素があればその中身、なければhtmlファイルの中身をアップロードする
    if len(pq_html("body")) > 0:
        html_data = pq_html("body").html()
    else:
        html_data = pq_html.html()

    output_html_file.parent.mkdir(exist_ok=True, parents=True)
    output_html_file.write_text(html_data, encoding="utf-8")


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    convert(args.input_html, args.output_html)


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(description="HTMLをConfluence用のXMLに変換します。")  # noqa: E501
    parser.add_argument(
        "input_html",
        type=Path,
        help="変換元の入力用HTML",
    )
    parser.add_argument(
        "output_html",
        type=Path,
        help="変換先の出力用HTML",
    )
    return parser


if __name__ == "__main__":
    main()
