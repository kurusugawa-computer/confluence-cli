from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Any

import confluence
from confluence.common.api import Api
from confluence.common.cli import create_api_instance

logger = logging.getLogger(__name__)


def create_attachments_from_file_list(
    api: Api, content_id: str, query_params: dict[str, Any], files: list[Path], filename_pattern: None | str, mime_type: None | str
) -> None:
    logger.info(f"{len(files)}件のファイルをアップロードします。")
    success_count = 0
    total_count = 0
    for file in files:
        if not file.is_file():
            logger.warning(f"'{file}'はファイルでないので、アップロードしません。")
            continue

        if filename_pattern is not None and not file.glob(filename_pattern):
            continue

        try:
            total_count += 1
            api.create_attachment(content_id, file, query_params=query_params, mime_type=mime_type)
            logger.debug(f"{total_count+1}件目: '{file}'をアップロードしました。")
        except Exception:
            logger.warning(f"'{file}'のアップロードに失敗しました。", exc_info=True)
            continue

        logger.debug(f"'{file}'をアップロードしました。")
        success_count += 1

    logger.info(f"{success_count}/{total_count} 件のファイルをアップロードしました。")


def create_attachments_from_directory(
    api: Api, content_id: str, query_params: dict[str, Any], directory: Path, filename_pattern: None | str, mime_type: None | str
) -> None:
    success_count = 0
    total_count = 0
    if not directory.is_dir():
        logger.error(f"'{directory}'はディレクトリでないので、終了します。")
        return

    logger.info(f"ディレクトリ'{directory}'内のファイルをアップロードします。")

    for file in directory.iterdir():
        if not file.is_file():
            continue
        if filename_pattern is not None and not file.glob(filename_pattern):
            continue
        try:
            total_count += 1
            api.create_attachment(content_id, file, query_params=query_params, mime_type=mime_type)
            logger.debug(f"{total_count}件目: '{file}'をアップロードしました。")
        except Exception:
            logger.warning(f"'{file}'のアップロードに失敗しました。", exc_info=True)
            continue
        success_count += 1

    logger.info(f"{success_count}/{total_count}件のファイルをアップロードしました。")


def main(args: argparse.Namespace) -> None:
    api = create_api_instance(args)
    content_id = args.content_id
    query_params = {"allowDuplicated": args.allow_duplicated}
    if args.file is not None:
        create_attachments_from_file_list(api, content_id, query_params, args.file, filename_pattern=args.filename_pattern, mime_type=args.mime_type)
    elif args.dir is not None:
        create_attachments_from_directory(api, content_id, query_params, args.dir, filename_pattern=args.filename_pattern, mime_type=args.mime_type)


def add_arguments_to_parser(parser: argparse.ArgumentParser):
    parser.add_argument("-c", "--content_id", required=True, help="ファイルのアップロード先であるページのcontent_id")

    file_group = parser.add_mutually_exclusive_group(required=True)
    file_group.add_argument("--file", type=Path, nargs="+", help="アップロードするファイル")
    file_group.add_argument("--dir", type=Path, help="アップロードするディレクトリ")

    parser.add_argument("--mime_type", type=str, help="ファイル名からMIMEタイプが判別できないときに、この値を添付ファイルのMIMEタイプとします。")

    parser.add_argument("--allow_duplicated", action="store_true", help="指定した場合は、すでに同じファイルが存在しても上書きします。")

    parser.add_argument("--filename_pattern", help="glob形式のパターンに一致するファイル名だけアップロードします。(ex) '*.png'")
    parser.set_defaults(subcommand_func=main)


def add_parser(subparsers: argparse._SubParsersAction | None = None) -> argparse.ArgumentParser:
    subcommand_name = "create"
    subcommand_help = "添付ファイルを作成します。"

    parser = confluence.common.cli.add_parser(subparsers, subcommand_name, subcommand_help)

    add_arguments_to_parser(parser)
    return parser
