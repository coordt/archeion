"""Tests for automated archiving of a URL."""

import pytest

from archeion import archive
from archeion.archivers import get_default_archivers
from archeion.index.models import Artifact, ArtifactStatus, Link

pytestmark = pytest.mark.django_db
archiver_count = len(get_default_archivers())


async def dummy_archiver(artifact: Artifact, overwrite: bool = False) -> Artifact:
    """Dummy archiver."""
    artifact.status = ArtifactStatus.SUCCEEDED
    artifact.output_path = "dummy_output_path.txt"
    return artifact


def test_get_links_with_pending():
    """Function should only return the links that have at least 1 artifact with a pending status."""
    initial_links = list(archive.get_links_with_status())
    assert not initial_links
    link = Link.objects.create(url="http://example.com", content_type="text/html")
    for archiver in get_default_archivers():
        link.artifacts.create(plugin_name=archiver.plugin_name)
    Link.objects.create(url="http://indexonly.com", content_type="text/html")

    links = archive.get_links_with_status()
    assert len(links) == 1


def test_archive_links_without_link(mocker):
    """Function should find all pending links if no link is provided."""
    mocker.patch("archeion.archive.get_archivers_map", return_value={"dummy": dummy_archiver})
    link1 = Link.objects.create(url="http://example.com", content_type="text/html")
    link1.artifacts.create(plugin_name="dummy")
    link2 = Link.objects.create(url="http://indexonly.com", content_type="text/html")
    link2.artifacts.create(plugin_name="dummy")

    assert Artifact.objects.filter(status=ArtifactStatus.PENDING).count() == 2

    archive.archive_links()

    assert Artifact.objects.filter(status=ArtifactStatus.PENDING).count() == 0
    assert Artifact.objects.filter(status=ArtifactStatus.SUCCEEDED).count() == 2


def test_archive_links_with_link(mocker):
    """Function should only archive the link provided."""
    mocker.patch("archeion.archive.get_archivers_map", return_value={"dummy": dummy_archiver})
    link1 = Link.objects.create(url="http://example.com", content_type="text/html")
    link1.artifacts.create(plugin_name="dummy")
    link2 = Link.objects.create(url="http://indexonly.com", content_type="text/html")
    link2.artifacts.create(plugin_name="dummy")

    assert Artifact.objects.filter(status=ArtifactStatus.PENDING).count() == 2

    archive.archive_links([link1])

    assert Artifact.objects.filter(status=ArtifactStatus.PENDING).count() == 1
    assert Artifact.objects.filter(status=ArtifactStatus.SUCCEEDED).count() == 1
