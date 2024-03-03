from pathlib import Path

from confluence.local.convert_html_to_xml import convert


def test__convert_img_elm():
    # 手間を省くため、assertしない
    convert(Path("tests/resources/page.html"), Path("tests/out/local/convert_html/page.xml"))
