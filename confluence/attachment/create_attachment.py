import argparse
import logging
from pathlib import Path

import confluence
from confluence.common.cli import create_api_instance

logger = logging.getLogger(__name__)


def main(args):
    api = create_api_instance(args)
    content_id = args.content_id
    if args.file is not None:
        files:list[Path] = args.file
        logger.info(f"{len(files)}件のファイルをアップロードします。")
        success_count = 0
        for file in files:
            if not file.is_file():
                logger.warning(f"'{file}'はファイルでないので、アップロードしません。")
                continue
            api.create_attachment(content_id, file, query_params={"allowDuplicated":args.allow_duplicated})
            logger.debug(f"'{file}'をアップロードしました。")
            success_count += 1

        logger.info(f"{success_count}件のファイルをアップロードします。")


def parse_args(parser: argparse.ArgumentParser):
    parser.add_argument("-c", "--content_id", required=True, help="ファイルのアップロード先であるページのcontent_id")

    file_group = parser.add_mutually_exclusive_group(required=True)
    file_group.add_argument("--file", type=Path, nargs="+", help="アップロードするファイル")
    file_group.add_argument("--dir", type=Path, help="アップロードするディレクトリ")

    parser.add_argument("--allow_duplicated", action="store_true",help="指定した場合は、すでに同じファイルが存在しても上書きします。")
    parser.set_defaults(subcommand_func=main)


def add_parser(subparsers: argparse._SubParsersAction | None = None) -> argparse.ArgumentParser:
    subcommand_name = "create"
    subcommand_help = "添付ファイルを作成します。"

    parser = confluence.common.cli.add_parser(subparsers, subcommand_name, subcommand_help)

    parse_args(parser)
    return parser
