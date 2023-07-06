"""
Command Line Interfaceの共通部分
"""
import argparse
import getpass
import logging
import os
from typing import Optional

from more_itertools import first_true

from confluence.common.api import Api

logger = logging.getLogger(__name__)

COMMAND_LINE_ERROR_STATUS_CODE = 2


class PrettyHelpFormatter(argparse.RawTextHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    def _format_action(self, action: argparse.Action) -> str:
        return super()._format_action(action) + "\n"

    def _get_help_string(self, action):  # noqa: ANN001
        """引数説明用のメッセージを生成する。
        不要なデフォルト値（--debug や オプショナルな引数）を表示させないようにする.
        `argparse.ArgumentDefaultsHelpFormatter._get_help_string` をオーバライドしている。

        Args:
            action ([type]): [description]

        Returns:
            [type]: [description]
        """
        # ArgumentDefaultsHelpFormatter._get_help_string の中身を、そのまま持ってきた。
        # https://qiita.com/yuji38kwmt/items/c7c4d487e3188afd781e 参照

        # 必須な引数には、引数の説明の後ろに"(required)"を付ける
        help = action.help  # pylint: disable=redefined-builtin  # noqa: A001
        if action.required:
            help += " (required)"  # noqa: A001

        if "%(default)" not in action.help:
            if action.default is not argparse.SUPPRESS:
                defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
                if action.option_strings or action.nargs in defaulting_nargs:
                    # 以下の条件だけ、annofabcli独自の設定
                    if action.default is not None and not action.const:
                        help += " (default: %(default)s)"  # noqa: A001
        return help


def add_parser(
    subparsers: Optional[argparse._SubParsersAction],
    command_name: str,
    command_help: str,
    description: Optional[str] = None,
    is_subcommand: bool = True,
    epilog: Optional[str] = None,
) -> argparse.ArgumentParser:
    """
    サブコマンド用にparserを追加する

    Args:
        subparsers: Noneの場合はsubparserを生成します。
        command_name:
        command_help: 1階層上のコマンドヘルプに表示される コマンドの説明（簡易的な説明）
        description: ヘルプ出力に表示される説明（詳細な説明）
        is_subcommand: サブコマンドかどうか. `annoworkcli job`はコマンド、`annoworkcli job list`はサブコマンドとみなす。
        epilog: ヘルプ出力後に表示される内容。デフォルトはNoneです。

    Returns:
        サブコマンドのparser

    """
    GLOBAL_OPTIONAL_ARGUMENTS_TITLE = "global optional arguments"

    def create_parent_parser() -> argparse.ArgumentParser:
        """
        共通の引数セットを生成する。
        """
        parent_parser = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
        group = parent_parser.add_argument_group(GLOBAL_OPTIONAL_ARGUMENTS_TITLE)
        group.add_argument("--debug", action="store_true", help="指定するとデバッグ用のログが出力されます。")
        group.add_argument(
            "--base_url",
            type=str,
            default="https://kurusugawa.jp/confluence",
            help="アクセスするConfluenceのURL。アクセスするURLは'{base_url}'/rest/api/...'です。",
        )
        group.add_argument("--confluence_user_name", type=str, help="Confluenceにログインする際のユーザー名")
        group.add_argument("--confluence_user_password", type=str, help="Confluenceにログインする際のパスワード")

        return parent_parser

    if subparsers is None:
        # ヘルプページにコマンドラインオプションを表示する`sphinx-argparse`ライブラリが実行するときは、subparsersがNoneになる。
        subparsers = argparse.ArgumentParser(allow_abbrev=False).add_subparsers()
    parents = [create_parent_parser()] if is_subcommand else []

    parser = subparsers.add_parser(
        command_name,
        parents=parents,
        description=description if description is not None else command_help,
        help=command_help,
        epilog=epilog,
        formatter_class=PrettyHelpFormatter,
    )
    parser.set_defaults(command_help=parser.print_help)

    # 引数グループに"global optional group"がある場合は、"--help"オプションをデフォルトの"optional"グループから、"global optional arguments"グループに移動する # noqa: E501
    # https://ja.stackoverflow.com/a/57313/19524
    global_optional_argument_group = first_true(parser._action_groups, pred=lambda e: e.title == GLOBAL_OPTIONAL_ARGUMENTS_TITLE)
    if global_optional_argument_group is not None:
        # optional グループの 0番目が help なので取り出す
        help_action = parser._optionals._group_actions.pop(0)
        assert help_action.dest == "help"
        # global optional group の 先頭にhelpを追加
        global_optional_argument_group._group_actions.insert(0, help_action)

    return parser


def prompt_yesno(msg: str) -> bool:
    """
    標準入力で yes, noを選択できるようにする。
    Args:
        msg: 確認メッセージ

    Returns:
        True: Yes, False: No

    """
    while True:
        choice = input(f"{msg} [y/N] : ")
        if choice == "y":
            return True

        elif choice == "N":
            return False


def prompt_yesnoall(msg: str) -> tuple[bool, bool]:
    """
    標準入力で yes, no, all(すべてyes)を選択できるようにする。
    Args:
        msg: 確認メッセージ

    Returns:
        Tuple[yesno, is_all]. yesno:Trueならyes. is_all: Trueならall.

    """
    while True:
        choice = input(f"{msg} [y/N/ALL] : ")
        if choice == "y":
            return True, False

        elif choice == "N":
            return False, False

        elif choice == "ALL":
            return True, True


def create_api_instance(args: argparse.Namespace) -> Api:
    base_url = args.base_url

    def with_command_line_user_name(confluence_user_name: str) -> Api:
        if args.confluence_user_password is not None:
            return Api(confluence_user_name, args.confluence_user_password, base_url)
        else:
            # コマンドライン引数にパスワードが指定されなければ、標準入力からパスワードを取得する
            confluence_user_password = ""
            while confluence_user_password == "":
                confluence_user_password = getpass.getpass("Enter Confluence Password: ")
            return Api(confluence_user_name, confluence_user_password, base_url)

    def with_environ_user_name(confluence_user_name: str) -> Api:
        if "CONFLUENCE_USER_PASSWORD" in os.environ:
            return Api(confluence_user_name, os.environ["CONFLUENCE_USER_PASSWORD"], base_url)
        else:
            # 環境変数にパスワードが指定されなければ、標準入力からパスワードを取得する
            confluence_user_password = ""
            while confluence_user_password == "":
                confluence_user_password = getpass.getpass("Enter Confluence Password: ")
            return Api(confluence_user_name, confluence_user_password, base_url)

    def with_stdin_user_name() -> Api:
        # 標準入力から認証情報を取得する
        confluence_user_name = ""
        while confluence_user_name == "":
            confluence_user_name = input("Enter Confluence User Name: ")

        confluence_user_password = ""
        while confluence_user_password == "":
            confluence_user_password = getpass.getpass("Enter Confluence Password: ")

        return Api(confluence_user_name, confluence_user_password, base_url)

    if args.confluence_user_name is not None:
        # コマンドラインから取得する
        return with_command_line_user_name(args.confluence_user_name)

    if "CONFLUENCE_USER_NAME" in os.environ:
        # 環境変数から取得する
        return with_environ_user_name(os.environ["CONFLUENCE_USER_NAME"])

    # 標準入力から認証情報を取得する
    return with_stdin_user_name()
