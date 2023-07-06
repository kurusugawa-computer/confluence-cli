import argparse
import logging
from typing import Any

import confluence
from confluence.common.api import Api
from confluence.common.cli import create_api_instance

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

    results: list[dict[str, Any]] = get_attachments(api, content_id, filename=args.filename, media_type=args.media_type)
    logger.info(f"{len(results)}件の添付ファイルを削除します。")

    for attachment in results:
        attachment_id = attachment["id"]
        attachment_title = attachment["title"]
        try:
            logger.debug(f"id='{attachment_id}', title='{attachment_title}'を削除します。 :: status='{attachment['status']}'")
            api.delete_content(attachment_id)
        except Exception:
            logger.warning(f"id='{attachment_id}', title='{attachment_title}'の削除に失敗しました。", exc_info=True)
            continue


def add_arguments_to_parser(parser: argparse.ArgumentParser):
    parser.add_argument("-c", "--content_id", required=True, help="ファイルのアップロード先であるページのcontent_id")

    parser.add_argument("--filename", help="filter parameter to return only the Attachment with the matching file name")
    parser.add_argument("--media_type", help="filter parameter to return only Attachments with a matching Media-Type")

    parser.set_defaults(subcommand_func=main)


def add_parser(subparsers: argparse._SubParsersAction | None = None) -> argparse.ArgumentParser:
    subcommand_name = "delete"
    subcommand_help = "添付ファイルを削除します。"

    parser = confluence.common.cli.add_parser(subparsers, subcommand_name, subcommand_help)

    add_arguments_to_parser(parser)
    return parser
