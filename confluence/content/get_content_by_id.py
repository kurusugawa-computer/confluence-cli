import argparse
import logging
from pathlib import Path

import confluence
from confluence.common.cli import create_api_instance
from confluence.common.utils import print_json

logger = logging.getLogger(__name__)


def main(args: argparse.Namespace) -> None:
    api = create_api_instance(args)
    content_id_list = args.content_id

    results = []
    for content_id in content_id_list:
        result = api.get_content_by_id(content_id, query_params={"status": "any"})
        results.append(result)

    print_json(results, is_pretty=True, output=args.output)


def add_arguments_to_parser(parser: argparse.ArgumentParser):
    parser.add_argument("-c", "--content_id", required=True, nargs="+", help="取得対象のコンテンツのID")

    parser.add_argument("-o", "--output", type=Path, help="出力先")

    parser.set_defaults(subcommand_func=main)


def add_parser(subparsers: argparse._SubParsersAction | None = None) -> argparse.ArgumentParser:
    subcommand_name = "get_by_id"
    subcommand_help = "コンテンツの情報を取得します。"

    parser = confluence.common.cli.add_parser(subparsers, subcommand_name, subcommand_help)

    add_arguments_to_parser(parser)
    return parser
