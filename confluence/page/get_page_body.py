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
    STORAGE = "storage"
    VIEW = "view"
    EDITOR = "editor"
    EXPORT_VIEW = "export_view"
    STYLED_VIEW = "styled_view"
    ANONYMOUS_EXPORT_VIEW = "anonymous_export_view"


def main(args: argparse.Namespace) -> None:
    api = create_api_instance(args)
    representation = args.representation
    expand = f"body.{representation}"
    content_id = args.content_id

    result = api.get_content_by_id(content_id, query_params={"expand": expand})

    output_string(result["body"][representation]["value"], output=args.output)


def add_arguments_to_parser(parser: argparse.ArgumentParser):
    parser.add_argument("-c", "--content_id", required=True, help="取得対象のコンテンツのID")
    parser.add_argument(
        "--representation", choices=[e.value for e in BodyRepresentation], default=BodyRepresentation.STORAGE.value, help="ページの中身の表現方法"
    )
    parser.add_argument("-o", "--output", type=Path, help="出力先")

    parser.set_defaults(subcommand_func=main)


def add_parser(subparsers: argparse._SubParsersAction | None = None) -> argparse.ArgumentParser:
    subcommand_name = "get_body"
    subcommand_help = "ページの中身を取得します。"

    parser = confluence.common.cli.add_parser(subparsers, subcommand_name, subcommand_help)

    add_arguments_to_parser(parser)
    return parser
