"""Tools for extracting HTML from a URL."""
import json
import os

from django.core.exceptions import SuspiciousFileOperation
from django.core.files.base import ContentFile

from archeion.index.models import ArtifactStatus, Link, Tag
from archeion.index.storage import get_artifact_storage
from archeion.logging import error, success
from archeion.post_processors.dandelion import get_dandelion_tags

PLUGIN_NAME = "html_metadata"


def save_html_metadata(content: str, link: Link, overwrite: bool = True) -> None:
    """
    Create an HTML metadata Artifact for a link.

    Args:
        content: The raw HTML content
        link: The link to save the metadata for
        overwrite: Whether to overwrite an existing metadata artifact
    """
    artifact, _ = link.artifacts.get_or_create(plugin_name=PLUGIN_NAME, defaults={"output_path": "html_metadata.json"})
    if artifact.status == ArtifactStatus.SUCCEEDED and not overwrite:
        return

    # Create the metadata
    metadata = parse_html_metadata(content, link.url)

    # Create the tags and add the tags to the link.tags
    for tag in metadata.get("tags", []):
        tag = Tag.objects.get_or_create(name=tag)
        link.tags.add(tag)

    # add or update the metadata to the link.metadata
    if link.metadata:
        link.metadata.update(metadata)
    else:
        link.metadata = metadata
    link.save()

    # save the artifact and metadata to storage
    try:
        storage = get_artifact_storage()
        filepath = os.path.join(link.archive_path, artifact.output_path)
        storage.save(filepath, ContentFile(json.dumps(metadata)))
        artifact.status = ArtifactStatus.SUCCEEDED
        success(f"Saved {PLUGIN_NAME} to {filepath}")
    except SuspiciousFileOperation as e:  # pragma: no coverage
        artifact.status = ArtifactStatus.FAILED
        error([f"{PLUGIN_NAME} failed:", e])


def parse_html_metadata(content: str, source: str) -> dict:
    """
    Extract post_processors from HTML content.

    Args:
        content: The content to process
        source: The URL source of the content

    Returns:
        The post_processors from the HTML document
    """
    from archeion.post_processors.html_metadata import Normalizer, extract_metadata

    page_source = strip_excess_elements(content)
    raw_metadata = extract_metadata(page_source, source)
    metadata = Normalizer(raw_metadata, source).normalized_metadata()
    metadata["keywords"] |= get_dandelion_tags(page_source, "text/html")
    return metadata


def strip_excess_elements(page_source: str) -> str:
    """
    Get rid of elements that do not provide any content.

    - style
    - script that are not json-ld

    Args:
        page_source: Raw HTML

    Returns:
        The HTML without those tags
    """
    from bs4 import BeautifulSoup

    def not_jsonld(element) -> bool:
        if element.name != "script":
            return False

        return not (element.has_attr("type") and element["type"] == "application/ld+json")

    soup = BeautifulSoup(page_source, "html.parser")

    for tag in soup.find_all("style"):
        tag.decompose()

    for tag in soup.find_all(not_jsonld):
        tag.decompose()

    return soup.prettify()
