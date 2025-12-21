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
    for index, file in enumerate(files):
        if not file.is_file():
            logger.warning(f"'{file}'はファイルでないので、アップロードしません。")
            continue

        if filename_pattern is not None and not file.glob(filename_pattern):
            continue

        try:
            api.create_attachment(content_id, file, query_params=query_params, mime_type=mime_type)
            logger.debug(f"{index+1}件目: '{file}'をアップロードしました。")
            if (index + 1) % 10 == 0:
                logger.info(f"{index+1}件目のファイルのアップロードが完了しました。")

        except Exception:
            logger.warning(f"'{file}'のアップロードに失敗しました。", exc_info=True)
            continue

        logger.debug(f"'{file}'をアップロードしました。")
        success_count += 1

    logger.info(f"{success_count}/{len(files)} 件のファイルをアップロードしました。")


def create_attachments_from_directory(
    api: Api, content_id: str, query_params: dict[str, Any], directory: Path, filename_pattern: None | str, mime_type: None | str
) -> None:
    success_count = 0
    if not directory.is_dir():
        logger.error(f"'{directory}'はディレクトリでないので、終了します。")
        return

    files = []
    for file in directory.iterdir():
        if not file.is_file():
            continue
        if filename_pattern is not None and not file.glob(filename_pattern):
            continue
        files.append(file)

    logger.info(f"ディレクトリ'{directory}'内のファイル{len(files)}件をアップロードします。")

    for index, file in enumerate(files):
        try:
            api.create_attachment(content_id, file, query_params=query_params, mime_type=mime_type)
            logger.debug(f"{index+1}件目: '{file}'をアップロードしました。")
            if (index + 1) % 10 == 0:
                logger.info(f"{index+1}件目のファイルのアップロードが完了しました。")

        except Exception:
            logger.warning(f"'{file}'のアップロードに失敗しました。", exc_info=True)
            continue
        success_count += 1

    logger.info(f"{success_count}/{len(files)}件のファイルをアップロードしました。")


def main(args: argparse.Namespace) -> None:
    api = create_api_instance(args)
    content_id = args.parent_content_id
    query_params = {"allowDuplicated": args.allow_duplicated}
    if args.file is not None:
        create_attachments_from_file_list(api, content_id, query_params, args.file, filename_pattern=args.filename_pattern, mime_type=args.mime_type)
    elif args.dir is not None:
        create_attachments_from_directory(api, content_id, query_params, args.dir, filename_pattern=args.filename_pattern, mime_type=args.mime_type)


def add_arguments_to_parser(parser: argparse.ArgumentParser):  # noqa: ANN201
    parser.add_argument("-c", "--parent_content_id", required=True, help="ファイルのアップロード先であるページのcontent_id")

    file_group = parser.add_mutually_exclusive_group(required=True)
    file_group.add_argument("--file", type=Path, nargs="+", help="アップロードするファイル")
    file_group.add_argument("--dir", type=Path, help="アップロードするディレクトリ")

    parser.add_argument("--mime_type", type=str, help="ファイル名からMIMEタイプが判別できないときに、この値を添付ファイルのMIMEタイプとします。")

    parser.add_argument(
        "--allow_duplicated",
        action="store_true",
        help="指定した場合は、アップロード先にすでに同じファイルが存在している場合に上書きます。指定しない場合は、400 Errorが発生します。",
    )

    parser.add_argument("--filename_pattern", help="glob形式のパターンに一致するファイル名だけアップロードします。(ex) '*.png'")
    parser.set_defaults(subcommand_func=main)


def add_parser(subparsers: argparse._SubParsersAction | None = None) -> argparse.ArgumentParser:
    subcommand_name = "create"
    subcommand_help = "添付ファイルを作成します。"

    parser = confluence.common.cli.add_parser(subparsers, subcommand_name, subcommand_help)

    add_arguments_to_parser(parser)
    return parser
