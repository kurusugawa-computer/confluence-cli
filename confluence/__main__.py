import logging

import click

import confluence
from confluence.command.address import address


def set_logger():
    logging_formatter = "%(levelname)-8s : %(asctime)s : %(filename)s : %(name)s : %(funcName)s : %(message)s"
    logging.basicConfig(format=logging_formatter)
    logging.getLogger(__package__).setLevel(level=logging.DEBUG)


@click.group()
@click.version_option(version=confluence.__version__)
def cli():
    set_logger()


cli.add_command(address)


if __name__ == "__main__":
    cli()
