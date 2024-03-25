"""Tests for the DOM archiver plugin."""

import asyncio
from pathlib import Path

import pytest

from archeion.archivers.dom import DOMArchiver
from archeion.index.models import ArtifactStatus, Link

pytestmark = pytest.mark.django_db


def test_dom_archiver(settings, tmp_path: Path, httpserver, fixture_dir: Path) -> None:
    """Test the DOM archiver."""
    settings.ARCHIVE_STORAGE_OPTIONS["location"] = tmp_path
    blog_content = fixture_dir.joinpath("blog.html").read_text()
    httpserver.serve_content(blog_content)

    link1 = Link.objects.create(url=httpserver.url, content_type="text/html")
    initial_artifact = link1.artifacts.create(plugin_name=DOMArchiver.plugin_name)

    archiver = DOMArchiver({})
    artifact = asyncio.run(archiver(initial_artifact))

    assert artifact.status == ArtifactStatus.SUCCEEDED
    assert artifact.output_path == "dom.html"
    output_path = tmp_path.joinpath(link1.archive_path).joinpath("dom.html")
    assert "Blog Template · Bootstrap v5.3" in output_path.read_text()[:372]
