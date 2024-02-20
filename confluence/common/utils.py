from __future__ import annotations

import json
import logging.config
import pkgutil
from pathlib import Path
from typing import Any, Optional, TypeVar

import yaml

logger = logging.getLogger(__name__)

T = TypeVar("T")  # Can be anything


def read_lines(filepath: str) -> list[str]:
    """ファイルを行単位で読み込む。改行コードを除く"""

    # BOM付きUTF-8のファイルも読み込めるようにする
    with open(filepath, encoding="utf-8-sig") as f:
        lines = f.readlines()
    return [e.rstrip("\r\n") for e in lines]


def read_lines_except_blank_line(filepath: str) -> list[str]:
    """ファイルを行単位で読み込む。ただし、改行コード、空行を除く"""
    lines = read_lines(filepath)
    return [line for line in lines if line != ""]


def output_string(target: str, output: Optional[Path] = None) -> None:
    """
    文字列を出力する。

    Args:
        target: 出力対象の文字列
        output: 出力先。Noneなら標準出力に出力する。
    """
    if output is None:
        print(target)
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open(mode="w", encoding="utf_8") as f:
            f.write(target)
            logger.info(f"{output} に出力しました。")


def print_json(target: Any, is_pretty: bool = False, output: Optional[Path] = None) -> None:  # noqa: ANN401
    """
    JSONを出力する。

    Args:
        target: 出力対象のJSON
        is_pretty: 人が見やすいJSONを出力するか
        output: 出力先。Noneなら標準出力に出力する。

    """
    if is_pretty:
        output_string(json.dumps(target, indent=2, ensure_ascii=False), output)
    else:
        output_string(json.dumps(target, ensure_ascii=False), output)


def set_logger(is_debug_mode: bool = False):
    """
    デフォルトのロガーを設定する。パッケージ内のlogging.yamlを読み込む。
    """
    data = pkgutil.get_data("confluence", "data/logging.yaml")
    if data is None:
        raise RuntimeError("confluence/data/logging.yaml の読み込みに失敗しました。")

    logging_config = yaml.safe_load(data.decode("utf-8"))

    if is_debug_mode:
        logging_config["loggers"]["confluence"]["level"] = "DEBUG"
        logging_config["loggers"]["__main__"]["level"] = "DEBUG"

    logging.config.dictConfig(logging_config)
