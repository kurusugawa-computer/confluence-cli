from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Any

import confluence
from confluence.common.cli import create_api_instance
from confluence.common.utils import print_json

logger = logging.getLogger(__name__)


def main(args: argparse.Namespace) -> None:
    api = create_api_instance(args)
    content_id = args.content_id
    expand = ",".join(args.expand) if args.expand else None

    limit = 50
    start = 0
    results: list[dict[str, Any]] = []
    while True:
        result = api.get_attachments(
            content_id, query_params={"filename": args.filename, "mediaType": args.media_type, "start": start, "limit": limit, "expand": expand}
        )
        results.extend(result["results"])
        if result["size"] < limit:
            break
        start = start + limit

    print_json(results, is_pretty=True, output=args.output)


def add_arguments_to_parser(parser: argparse.ArgumentParser):
    parser.add_argument("-c", "--content_id", required=True, help="取得した添付ファイルが存在するページのcontent_id")

    parser.add_argument("--filename", help="filter parameter to return only the Attachment with the matching file name")
    parser.add_argument("--media_type", help="filter parameter to return only Attachments with a matching Media-Type")

    parser.add_argument("--expand", nargs="+", help="取得したい情報のプロパティ。指定できる値は出力結果の`_expandable`を参照してください。")

    parser.add_argument("-o", "--output", type=Path, help="出力先")

    parser.set_defaults(subcommand_func=main)


def add_parser(subparsers: argparse._SubParsersAction | None = None) -> argparse.ArgumentParser:
    subcommand_name = "get"
    subcommand_help = "添付ファイルの情報を取得します。"

    parser = confluence.common.cli.add_parser(subparsers, subcommand_name, subcommand_help)

    add_arguments_to_parser(parser)
    return parser
