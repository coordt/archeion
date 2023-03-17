"""Run post-processing methods on all DOM artifacts."""
from django.core.management.base import BaseCommand

from archeion.index.models import ArtifactStatus, Link
from archeion.post_process import post_process_links


class Command(BaseCommand):
    """Post-process DOM artifacts."""

    help = "Post-process DOM artifacts."

    def __init__(self, *args, **kwargs):
        from archeion.archivers import get_archivers_map

        super().__init__(*args, **kwargs)
        self.archivers = get_archivers_map()

    def add_arguments(self, parser):
        """Add the command's arguments to the parser."""
        pass

    def handle(self, *args, **options):
        """Run the command."""
        from archeion.logging import info

        links = Link.objects.filter(artifacts__status=ArtifactStatus.SUCCEEDED, artifacts__plugin_name="DOM")
        info(f"Post-processing {len(links)} links...")
        post_process_links(links)
