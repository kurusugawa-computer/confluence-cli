from __future__ import annotations

import argparse
import logging
from difflib import unified_diff
from pathlib import Path
from urllib.parse import urlencode

from confluence.common import cli
from confluence.common.cli import create_api_instance, prompt_yesno
from confluence.common.utils import output_string, print_json

logger = logging.getLogger(__name__)


def storage_diff(current_body: str, edited_body: str) -> str:
    lines = unified_diff(current_body.splitlines(keepends=True), edited_body.splitlines(keepends=True), fromfile="current", tofile="edited")
    return "".join(line if line.endswith("\n") else f"{line}\n\\ No newline at end of file\n" for line in lines)


def main(args: argparse.Namespace) -> None:
    api = create_api_instance(args)
    page_id = args.page_id
    xml_file: Path = args.xml_file
    comment = args.comment if args.comment is not None else "Updated via confluence-cli"
    xml_text = xml_file.read_text(encoding="utf-8")

    old_content = api.get_content_by_id(page_id, query_params={"expand": "version,ancestors,space,body.storage"})

    page_title = old_content["title"]
    page_info = {
        "page_id": page_id,
        "title": page_title,
        "url": f"{api.base_url}/pages/viewpage.action?{urlencode({'pageId': page_id})}",
    }
    if args.dry_run:
        version = old_content["version"]["number"]
        diff = storage_diff(old_content["body"]["storage"]["value"], xml_text)
        if args.json:
            print_json({**page_info, "status": "preview", "version": version, "diff": diff})
        else:
            output_string(f"{page_title} (ID: {page_id}, 版: {version})\n{page_info['url']}\n{diff or '本文に変更はありません。'}".rstrip("\n"))
        return

    space_key = old_content["space"]["key"]
    logger.info(f"次のページを更新します。 :: page_id='{page_id}', title='{page_title}', space.key='{space_key}'")

    if not args.yes:
        if not prompt_yesno("ページを更新しますか?"):
            logger.info("ページの更新をキャンセルしました。")
            if args.json:
                print_json({**page_info, "status": "cancelled", "version": old_content["version"]["number"]})
            return

    request_body = {
        "version": {"number": old_content["version"]["number"] + 1, "message": comment},
        "title": page_title,
        "type": old_content["type"],
        "space": {"key": space_key},
        "body": {"storage": {"value": xml_text, "representation": "storage"}},
    }
    updated = api.update_content(page_id, request_body=request_body)
    if args.json:
        print_json({**page_info, "status": "updated", "version": updated["version"]["number"]})
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

    parser.add_argument("--dry_run", action="store_true", help="ページを更新せず、対象ページと本文の差分を出力します。")
    parser.add_argument("--json", action="store_true", help="プレビューまたは更新結果をJSONで出力します。")

    parser.set_defaults(subcommand_func=main)


def add_parser(subparsers: argparse._SubParsersAction | None = None) -> argparse.ArgumentParser:
    subcommand_name = "update"
    subcommand_help = "ページを更新します。"

    parser = cli.add_parser(subparsers, subcommand_name, subcommand_help)

    add_arguments_to_parser(parser)
    return parser
