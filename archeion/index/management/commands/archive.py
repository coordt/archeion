"""Archives any pending or failed Artifacts."""
from argparse import ArgumentParser

from asgiref.sync import async_to_sync
from django.core.management.base import BaseCommand
from django.db.models import Q

from archeion.index.models import Artifact, ArtifactStatus


class Command(BaseCommand):
    """Archives any pending or failed Artifacts."""

    help = "Archives any pending or failed Artifacts."

    def __init__(self, *args, **kwargs):
        from archeion.archivers import get_archivers_map

        super().__init__(*args, **kwargs)
        self.archivers = get_archivers_map()

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Add the command's arguments to the parser."""
        parser.add_argument("--no-failed", action="store_true", help="Do not attempt failed artifacts.")

    def handle(self, *args, **options) -> None:
        """Archives any pending or failed Artifacts."""
        from archeion.logging import info

        if options["no_failed"]:
            info("Skipping failed artifacts...")
            filter_query = Q(status=ArtifactStatus.PENDING)
        else:
            filter_query = Q(status=ArtifactStatus.FAILED) | Q(status=ArtifactStatus.PENDING)
        artifacts = Artifact.objects.filter(filter_query).select_related("link")

        info(f"Archiving {len(artifacts)} non-successful artifacts...")
        for art in artifacts:
            finished_artifact = self.archive(art)
            finished_artifact.save()

    @async_to_sync
    async def archive(self, artifact: Artifact) -> Artifact:
        """Archive a single artifact."""
        from archeion.logging import info

        info(f"Archiving {artifact.link.url} with {artifact.plugin_name}...", left_indent=2)
        return await self.archivers[artifact.plugin_name](artifact, False)
