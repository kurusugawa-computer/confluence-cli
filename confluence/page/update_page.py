from __future__ import annotations

import argparse
import logging
from pathlib import Path

from confluence.common import cli
from confluence.common.cli import create_api_instance, prompt_yesno

logger = logging.getLogger(__name__)


def main(args: argparse.Namespace) -> None:
    api = create_api_instance(args)
    page_id = args.page_id
    xml_file: Path = args.xml_file
    comment = args.comment if args.comment is not None else "Updated via confluence-cli"
    xml_text = xml_file.read_text(encoding="utf-8")

    old_content = api.get_content_by_id(page_id, query_params={"expand": "version,ancestors,space,body.storage"})

    page_title = old_content["title"]
    space_key = old_content["space"]["key"]
    logger.info(f"次のページを更新します。 :: page_id='{page_id}', title='{page_title}', space.key='{space_key}'")

    if not args.yes:
        if not prompt_yesno("ページを更新しますか?"):
            logger.info("ページの更新をキャンセルしました。")
            return

    request_body = {
        "version": {"number": old_content["version"]["number"] + 1, "message": comment},
        "title": page_title,
        "type": old_content["type"],
        "space": {"key": space_key},
        "body": {"storage": {"value": xml_text, "representation": "storage"}},
    }
    _ = api.update_content(page_id, request_body=request_body)
    logger.info(f"次のページを'{xml_file}'の内容で更新しました。 :: page_id='{page_id}', title='{page_title}', space.key='{space_key}'")


def add_arguments_to_parser(parser: argparse.ArgumentParser):  # noqa: ANN201
    parser.add_argument("-p", "--page_id", required=True, help="更新対象のページまたはブログのID")
    parser.add_argument(
        "--xml_file",
        required=True,
        type=Path,
        help="storageフォーマットで記載されたXMLファイルのパス。このファイルの内容でページが更新されます。",
    )
    parser.add_argument("--comment", help="ページを更新したときに残すコメント。")
    parser.add_argument("--yes", action="store_true", help="すべてのプロンプトに自動的に'yes'と答え、非対話的に実行します。")

    parser.set_defaults(subcommand_func=main)


def add_parser(subparsers: argparse._SubParsersAction | None = None) -> argparse.ArgumentParser:
    subcommand_name = "update"
    subcommand_help = "ページを更新します。"

    parser = cli.add_parser(subparsers, subcommand_name, subcommand_help)

    add_arguments_to_parser(parser)
    return parser
