"""Archeion Command line interface."""

import rich_click as click

from archeion import __version__


@click.group()
@click.version_option(version=__version__)
def cli() -> None:
    """An archive of documents."""
    pass
