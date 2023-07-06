import argparse
import logging
import sys
from typing import Optional, Sequence

import confluence
import confluence.attachment.subcommand

logger = logging.getLogger(__name__)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Command Line Interface for Confluence", formatter_class=PrettyHelpFormatter, allow_abbrev=False
    )
    parser.add_argument("--version", action="version", version=f"confluence {confluence.__version__}")
    parser.set_defaults(command_help=parser.print_help)

    subparsers = parser.add_subparsers(dest="command_name")

    confluence.attachment.subcommand.add_parser(subparsers)
    return parser


def main(arguments: Optional[Sequence[str]] = None):
    parser = create_parser()
    if arguments is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(arguments)

    if hasattr(args, "subcommand_func"):
        try:
            set_default_logger(is_debug_mode=args.debug)
            logger.info(f"{sys.argv=}")
            args.subcommand_func(args)
        except Exception as e:
            logger.exception(e)
            raise e

    else:
        # 未知のサブコマンドの場合はヘルプを表示
        args.command_help()


if __name__ == "__main__":
    main()
