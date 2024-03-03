import pytest
from confluence.__main__ import main
from confluence.local.convert_html_to_xml import convert
from pathlib import Path

def test__convert_img_elm():
    # 手間を省くため、assertしない
    convert(Path("tests/resources/page.html"), Path("tests/out/local/convert_html/page.xml"))
