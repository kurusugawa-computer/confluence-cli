import argparse
import logging
from pathlib import Path

import confluence
from confluence.common.cli import create_api_instance

logger = logging.getLogger(__name__)


def main(args):
    api = create_api_instance(args)

    GetMyAccount(
        annowork_service=annowork_service,
    ).main(output=args.output)


def parse_args(parser: argparse.ArgumentParser):
    parser.add_argument("-o", "--output", type=Path, required=False, help="出力先")

    parser.set_defaults(subcommand_func=main)


def add_parser(subparsers: argparse._SubParsersAction | None = None) -> argparse.ArgumentParser:
    subcommand_name = "create"
    subcommand_help = "添付ファイルを作成します。"

    parser = confluence.common.cli.add_parser(subparsers, subcommand_name, subcommand_help)

    parse_args(parser)
    return parser
