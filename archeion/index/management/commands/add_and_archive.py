"""Add and archive a URL or list of URLs."""
from argparse import ArgumentParser

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Add and archive a URL or list of URLs."""

    help = "Add and archive a URL or list of URLs."

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Add the command's arguments to the parser."""
        parser.add_argument("url_or_file", nargs="+")

    def handle(self, *args, **options) -> None:
        """Add and archive some URLs."""
        from archeion.add import add_links
        from archeion.archive import archive_links
        from archeion.post_process import post_process_links

        for url_or_file in options["url_or_file"]:
            links = add_links(url_or_file)
            if links:
                archive_links(links)
                post_process_links(links)
