from __future__ import annotations

import argparse
from typing import Optional

import confluence
import confluence.attachment.get_attachment
import confluence.local.convert_html_to_xml


def add_arguments_to_parser(parser: argparse.ArgumentParser):
    subparsers = parser.add_subparsers(dest="subcommand_name")

    # サブコマンドの定義
    confluence.local.convert_html_to_xml.add_parser(subparsers)


def add_parser(subparsers: Optional[argparse._SubParsersAction] = None) -> argparse.ArgumentParser:
    subcommand_name = "local"
    subcommand_help = "Confluenceにアクセスせずにローカル上で完結するコマンド"

    parser = confluence.common.cli.add_parser(subparsers, subcommand_name, subcommand_help, description=subcommand_help, is_subcommand=False)
    add_arguments_to_parser(parser)
    return parser
