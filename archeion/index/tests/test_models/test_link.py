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
