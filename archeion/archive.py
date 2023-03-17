"""Methods for archiving Links into the index."""
from typing import List, Optional

import asyncio

from asgiref.sync import async_to_sync
from django.db.models import QuerySet

from archeion.archivers import get_archivers_map
from archeion.index.models import Artifact, ArtifactStatus, Link
from archeion.logging import error, info


def get_links_with_status(status: ArtifactStatus = ArtifactStatus.PENDING) -> QuerySet:  # type: ignore[assignment]
    """Get all Links with pending status."""
    return Link.objects.filter(artifacts__status=status).order_by("-created_at").distinct()


def archive_links(links: Optional[List[Link]] = None, overwrite=False):
    """Archive links."""
    if links is None:
        links = get_links_with_status(ArtifactStatus.PENDING)  # type: ignore[arg-type]
        info("Archiving links with pending artifacts...")
    else:
        info(f"Archiving {len(links)} links...")

    for link in links:
        info(f"Archiving link {link.url}...", left_indent=2)

        # Each archiver logs its own information
        artifacts = list(link.artifacts.filter(status=ArtifactStatus.PENDING))
        finished_artifacts = _run_archivers(artifacts, overwrite)

        for artifact in finished_artifacts:
            artifact.save()


@async_to_sync
async def _run_archivers(artifacts: List[Artifact], overwrite: bool = False) -> List[Artifact]:
    """Run archivers for a list of artifacts."""
    archivers = get_archivers_map()
    tasks = [archivers[art.plugin_name](art, overwrite) for art in artifacts]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    outputs = []
    for result in results:
        if isinstance(result, BaseException):
            error([f"Archiver {result.__class__.__name__} raised an error:", str(result)])
        elif not isinstance(result, Artifact):
            error(f"Archiver {result.__class__.__name__} returned a non-Artifact: {result}")
        else:
            outputs.append(result)
    return outputs
