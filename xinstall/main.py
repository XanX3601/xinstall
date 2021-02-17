import click
import rich.logging
import logging


@click.group()
def cli():
    pass


def main():
    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[rich.logging.RichHandler()],
    )

    cli()
