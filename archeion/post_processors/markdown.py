"""Convert an HTML document to Markdown."""
import os

from django.core.exceptions import SuspiciousFileOperation
from django.core.files.base import ContentFile
from django.utils import timezone

from archeion.index.models import ArtifactStatus, Link
from archeion.index.storage import get_artifact_storage
from archeion.logging import error, success

PLUGIN_NAME = "markdown"


def convert_to_markdown(content: str, link: Link, overwrite: bool = True) -> None:
    """
    Convert HTML to Markdown.

    Args:
        content: HTML content
        link: Source link
        overwrite: Whether to overwrite an existing metadata artifact
    """
    import html2text

    artifact, _ = link.artifacts.get_or_create(
        plugin_name=PLUGIN_NAME, defaults={"output_path": "markdown.md", "start_ts": timezone.now()}
    )
    if artifact.status == ArtifactStatus.SUCCEEDED and not overwrite:
        return

    text_maker = html2text.HTML2Text()
    text_maker.unicode_snob = True
    text_maker.protect_links = True
    text_maker.mark_code = True
    output = text_maker.handle(content)

    try:
        storage = get_artifact_storage()
        filepath = os.path.join(link.archive_path, artifact.output_path)
        storage.save(filepath, ContentFile(output))
        artifact.status = ArtifactStatus.SUCCEEDED
        success(f"Saved {PLUGIN_NAME} to {filepath}")
    except SuspiciousFileOperation as e:  # pragma: no coverage
        artifact.status = ArtifactStatus.FAILED
        artifact.save()
        error([f"{PLUGIN_NAME} failed:", e])

    artifact.end_ts = timezone.now()
    artifact.save()
