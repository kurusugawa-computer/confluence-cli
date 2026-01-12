import argparse
import logging
from enum import Enum
from pathlib import Path

from lxml import etree, html

from confluence.common import cli
from confluence.common.cli import create_api_instance
from confluence.common.utils import output_string

logger = logging.getLogger(__name__)


class BodyRepresentation(Enum):
    """
    ページの中身の表現方法。
    各フィールドの説明は以下のドキュメントの説明を引用しています。
    https://docs.atlassian.com/atlassian-confluence/6.6.0/com/atlassian/confluence/api/model/content/ContentRepresentation.html
    """

    STORAGE = "storage"
    """Raw database format, for content that stores data in our XML storage format"""
    VIEW = "view"
    """HTML representation for viewing in a web page"""
    EDITOR = "editor"
    """Representation suitable for use in the rich text editor"""
    EXPORT_VIEW = "export_view"
    """HTML representation for viewing, but with absolute urls, instead of relative urls in the markup."""
    STYLED_VIEW = "styled_view"
    """A rendered view that includes inline styles in a <style> element, wrapped in an entire <html> structure."""
    ANONYMOUS_EXPORT_VIEW = "anonymous_export_view"
    """HTML representation for viewing, but with absolute urls, instead of relative urls in the markup, and macros are rendered as though it is viewed by an anonymous user."""  # noqa: E501


def format_html(content: str) -> str:
    """
    HTMLを整形します。

    Args:
        content: 整形対象のHTML文字列

    Returns:
        整形されたHTML文字列
    """
    try:
        # HTMLフラグメントをパースして整形
        root = html.fromstring(content)
        etree.indent(root, space="  ")
        return html.tostring(root, encoding="unicode")
    except Exception:
        logger.warning("HTML整形に失敗しました。", exc_info=True)
        return content


def main(args: argparse.Namespace) -> None:
    api = create_api_instance(args)
    representation = args.representation
    expand = f"body.{representation}"
    page_id = args.page_id

    result = api.get_content_by_id(page_id, query_params={"expand": expand})
    logger.info(f"以下のページの中身を取得しました。 :: page_id='{result['id']}', type='{result['type']}', title='{result['title']}'")
    content = result["body"][representation]["value"]

    # 整形オプションが指定されている場合は整形する
    if args.pretty:
        content = format_html(content)

    output_string(content, output=args.output)


def add_arguments_to_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("-p", "--page_id", required=True, help="取得対象のページまたはブログのID")
    parser.add_argument(
        "--representation",
        choices=[e.value for e in BodyRepresentation],
        default=BodyRepresentation.STORAGE.value,
        help="ページの中身の表現方法。詳細は https://qiita.com/yuji38kwmt/items/4ec92a024ea23a4bb378 を参照してください。",
    )
    parser.add_argument("-o", "--output", type=Path, help="出力先")
    parser.add_argument("--pretty", action="store_true", help="HTMLを整形して出力します。")

    parser.set_defaults(subcommand_func=main)


def add_parser(subparsers: argparse._SubParsersAction | None = None) -> argparse.ArgumentParser:
    subcommand_name = "get_body"
    subcommand_help = "ページまたはブログの中身を取得します。"

    parser = cli.add_parser(subparsers, subcommand_name, subcommand_help)

    add_arguments_to_parser(parser)
    return parser
