import argparse
from typing import Optional

import confluence
import confluence.attachment.create_attachment


def parse_args(parser: argparse.ArgumentParser):
    subparsers = parser.add_subparsers(dest="subcommand_name")

    # サブコマンドの定義
    confluence.attachment.create_attachment.add_parser(subparsers)


def add_parser(subparsers: Optional[argparse._SubParsersAction] = None) -> argparse.ArgumentParser:
    subcommand_name = "attachment"
    subcommand_help = "添付ファイルに関するサブコマンド"

    parser = confluence.common.cli.add_parser(subparsers, subcommand_name, subcommand_help, description=subcommand_help, is_subcommand=False)
    parse_args(parser)
    return parser
