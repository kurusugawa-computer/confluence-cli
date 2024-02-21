from __future__ import annotations

import argparse
from typing import Optional

import confluence
import confluence.page.get_page_body
import confluence.page.update_page


def add_arguments_to_parser(parser: argparse.ArgumentParser):
    subparsers = parser.add_subparsers(dest="subcommand_name")

    # サブコマンドの定義
    confluence.page.get_page_body.add_parser(subparsers)
    # 動かないので一旦コメントアウトする
    confluence.page.update_page.add_parser(subparsers)


def add_parser(subparsers: Optional[argparse._SubParsersAction] = None) -> argparse.ArgumentParser:
    subcommand_name = "page"
    subcommand_help = "ページに関するサブコマンド"

    parser = confluence.common.cli.add_parser(subparsers, subcommand_name, subcommand_help, description=subcommand_help, is_subcommand=False)
    add_arguments_to_parser(parser)
    return parser
