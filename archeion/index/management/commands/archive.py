"""Archives any pending or failed Artifacts."""
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

    def handle(self, *args, **options):
        """Archives any pending or failed Artifacts."""
        from archeion.logging import info

        artifacts = Artifact.objects.filter(
            Q(status=ArtifactStatus.FAILED) | Q(status=ArtifactStatus.PENDING)
        ).select_related("link")
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
