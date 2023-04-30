"""Initialize the archive."""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Initialize the archive."""

    help = "Initialize the archive."

    def handle(self, *args, **options) -> None:
        """This is where the action happens."""
        from archeion import config
        from archeion.index import setup

        default_settings = config.get_default_settings()
        setup.init(default_settings.archive_root)
