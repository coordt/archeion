"""Test the Link model."""

import pytest
from django.conf import settings

from archeion.index.models import Link

from ..factories import ArtifactFactory, LinkFactory

pytestmark = pytest.mark.django_db


def test_link_model(httpserver, fixture_dir):
    """Test the basic attributes of the Link model."""
    httpserver.serve_content(
        (fixture_dir / "example.com.html").read_text(), headers={"Content-Type": "text/html; charset=utf-8"}
    )
    link = Link.objects.create(url=httpserver.url)
    assert link.url == httpserver.url
    assert link.content_type == "text/html; charset=utf-8"
    assert link.parsed_url[0] == "http"
    assert link.parsed_url[1].startswith("127.0.0.1")
    assert f"{link}" == httpserver.url


def test_update_metadata():
    """Updating the metadata sets tags, title and ld_type."""
    link = Link.objects.create(
        url="http://foobar.org/",
        content_type="text/html; charset=utf-8",
    )
    assert link.title is None
    assert link.tags.count() == 0
    assert link.ld_type is None

    link.update_metadata({"type": "http://schema.org/Article"})
    link.save()
    assert link.title is None
    assert link.tags.count() == 0
    assert link.ld_type == "http://schema.org/Article"

    link.update_metadata({"headline": "This is an example headline"})
    link.save()
    assert link.title == "This is an example headline"
    assert link.tags.count() == 0
    assert link.ld_type == "http://schema.org/Article"

    link.update_metadata(({"keywords": ["foo", "bar", "baz"]}))
    link.save()
    assert link.title == "This is an example headline"
    assert link.tags.count() == 3
    assert link.ld_type == "http://schema.org/Article"
