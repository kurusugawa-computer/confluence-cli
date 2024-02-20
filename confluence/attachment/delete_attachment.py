from __future__ import annotations

import argparse
import logging
from typing import Any

import confluence
from confluence.common.api import Api
from confluence.common.cli import create_api_instance, prompt_yesnoall

logger = logging.getLogger(__name__)


def get_attachments(api: Api, content_id: str, *, filename: None | str, media_type: None | str) -> list[dict[str, Any]]:
    limit = 50
    start = 0
    results: list[dict[str, Any]] = []
    while True:
        result = api.get_attachments(content_id, query_params={"filename": filename, "mediaType": media_type, "start": start, "limit": limit})
        results.extend(result["results"])
        if result["size"] < limit:
            break
        start = start + limit
    return results


def main(args: argparse.Namespace) -> None:
    api = create_api_instance(args)
    content_id = args.content_id

    page = api.get_content_by_id(content_id)
    results: list[dict[str, Any]] = get_attachments(api, content_id, filename=args.filename, media_type=args.media_type)
    if len(results) == 0:
        logger.info(f"page title='{page['title']}'の削除対象の添付ファイルは0件なので、終了します。")
        return

    logger.info(f"page title='{page['title']}'の添付ファイル{len(results)}件を削除します。")

    is_purged = args.purge
    success_count = 0

    all_yes = False
    for index, attachment in enumerate(results):
        attachment_id = attachment["id"]
        attachment_title = attachment["title"]
        try:
            if not all_yes:
                confirm_message = f"id='{attachment_id}', title='{attachment_title}'を削除しますか？"
                if is_purged:
                    confirm_message += "ゴミ箱からも完全に削除します。復元できません。"
                else:
                    confirm_message += "ゴミ箱に移動します。"

                yes, all_yes = prompt_yesnoall(confirm_message)
            if yes or all_yes:
                logger.debug(f"{index+1}件目: id='{attachment_id}', title='{attachment_title}'をゴミ箱に移動します。 ")
                api.delete_content(attachment_id, query_params={"status": "current"})
                if is_purged:
                    logger.debug(f"{index+1}件目: id='{attachment_id}', title='{attachment_title}'をゴミ箱から完全に削除します。 ")
                    api.delete_content(attachment_id, query_params={"status": "trashed"})
                success_count += 1

        except Exception:
            logger.warning(f"{index+1}件目: id='{attachment_id}', title='{attachment_title}'の削除に失敗しました。", exc_info=True)
            continue

    logger.info(f"{success_count}/{len(results)} 件の添付ファイルを削除しました。")


def add_arguments_to_parser(parser: argparse.ArgumentParser):
    parser.add_argument("-c", "--content_id", required=True, help="削除したい添付ファイルが存在するページのcontent_id")

    parser.add_argument("--filename", help="filter parameter to return only the Attachment with the matching file name")
    parser.add_argument("--media_type", help="filter parameter to return only Attachments with a matching Media-Type")
    parser.add_argument("--purge", action="store_true", help="指定すると、ゴミ箱からも完全に削除します。復元できません。")
    parser.set_defaults(subcommand_func=main)


def add_parser(subparsers: argparse._SubParsersAction | None = None) -> argparse.ArgumentParser:
    subcommand_name = "delete"
    subcommand_help = "添付ファイルを削除します。"

    parser = confluence.common.cli.add_parser(subparsers, subcommand_name, subcommand_help)

    add_arguments_to_parser(parser)
    return parser
