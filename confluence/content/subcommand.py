from __future__ import annotations

import argparse
from typing import Optional

import confluence
import confluence.content.get_content_by_id


def add_arguments_to_parser(parser: argparse.ArgumentParser):
    subparsers = parser.add_subparsers(dest="subcommand_name")

    # サブコマンドの定義
    confluence.content.get_content_by_id.add_parser(subparsers)


def add_parser(subparsers: Optional[argparse._SubParsersAction] = None) -> argparse.ArgumentParser:
    subcommand_name = "content"
    subcommand_help = "コンテンツ（ページ、ブログ、添付ファイルなど）に関するサブコマンド"

    parser = confluence.common.cli.add_parser(subparsers, subcommand_name, subcommand_help, description=subcommand_help, is_subcommand=False)
    add_arguments_to_parser(parser)
    return parser
