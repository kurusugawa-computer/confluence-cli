import logging

import click

logger = logging.getLogger(__name__)


def power(num: int):
    """べき乗を返します

    Args:
        num (int): 数値

    Returns:
        べき乗
    """
    return num * num


@click.command(name="address", help="住所を出力します。")
@click.option(
    "--postcode",
    type=bool,
    is_flag=True,
    help="郵便番号も出力します。",
)
def address(postcode: bool):
    logger.debug("'address' command が実行されました。")
    msg = "愛知県名古屋市中区新栄一丁目29-23 アーバンドエル新栄2階"
    if postcode:
        msg = "〒460-0007 " + msg
    click.echo(msg)
