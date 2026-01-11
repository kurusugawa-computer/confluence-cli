from __future__ import annotations

import argparse
import logging
from enum import Enum
from pathlib import Path

import confluence
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
    """A rendered view that includes inline styles in a"""
    ANONYMOUS_EXPORT_VIEW = "anonymous_export_view"
    """HTML representation for viewing, but with absolute urls, instead of relative urls in the markup, and macros are rendered as though it is viewed by an anonymous user."""  # noqa: E501


def main(args: argparse.Namespace) -> None:
    api = create_api_instance(args)
    representation = args.representation
    expand = f"body.{representation}"
    page_id = args.page_id

    result = api.get_content_by_id(page_id, query_params={"expand": expand})

    output_string(result["body"][representation]["value"], output=args.output)


def add_arguments_to_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("-p", "--page_id", required=True, help="取得対象のページまたはブログのID")
    parser.add_argument(
        "--representation", choices=[e.value for e in BodyRepresentation], default=BodyRepresentation.STORAGE.value, help="ページの中身の表現方法"
    )
    parser.add_argument("-o", "--output", type=Path, help="出力先")

    parser.set_defaults(subcommand_func=main)


def add_parser(subparsers: argparse._SubParsersAction | None = None) -> argparse.ArgumentParser:
    subcommand_name = "get_body"
    subcommand_help = "ページまたはブログの中身を取得します。"

    parser = confluence.common.cli.add_parser(subparsers, subcommand_name, subcommand_help)

    add_arguments_to_parser(parser)
    return parser
