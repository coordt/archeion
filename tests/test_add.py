"""Tests the adding of links to the archive."""

import pytest
from httpx import Response

from archeion.add import add_links
from archeion.archivers import get_default_archivers
from archeion.index.models import Artifact, Link

pytestmark = pytest.mark.django_db
archiver_count = len(get_default_archivers())


def test_add_links_no_links(mocker, capsys):
    """Trying to add an empty string should result in no links added."""
    links = add_links("")
    captured = capsys.readouterr()
    output = [line.rstrip() for line in captured.out.splitlines()]
    assert output == [
        "ℹ Parsing input",
        "  ℹ Parsed 0 URLs from input",
    ]
    assert len(links) == 0
    assert Link.objects.count() == 0
    assert Artifact.objects.count() == 0


def test_add_links_url(mocker, capsys):
    """Adding a URL should add a link to the archive."""
    mock_httpx = mocker.patch("archeion.index.models.httpx")
    mock_httpx.head.return_value = Response(status_code=200, headers={"content-type": "text/html"}, content="")

    links = add_links("https://example.com")
    captured = capsys.readouterr()
    output = [line.rstrip() for line in captured.out.splitlines()]
    assert output == [
        "ℹ Parsing input",
        "  ℹ Parsed 1 URLs from input",
        "  ℹ Found 1 new URLs not already in index",
    ]
    assert len(links) == 1
    assert Link.objects.count() == 1
    assert Artifact.objects.count() == archiver_count


def test_add_links_urllist(mocker, capsys, fixture_dir):
    """Adding a file of URLs should add a links to the archive."""
    mock_httpx = mocker.patch("archeion.index.models.httpx")
    mock_httpx.head.return_value = Response(status_code=200, headers={"content-type": "text/html"}, content="")
    links = add_links(str(fixture_dir / "url-list.txt"))
    captured = capsys.readouterr()
    output = [line.rstrip() for line in captured.out.splitlines()]
    assert output == [
        "ℹ Parsing input",
        "  ℹ Parsed 8 URLs from input",
        "  ℹ Found 8 new URLs not already in index",
    ]
    assert len(links) == 8
    assert Link.objects.count() == 8
    assert Link.objects.get(url="https://farrell-turner.info/")
    assert Artifact.objects.count() == archiver_count * 8


def test_add_links_url_already_in_archive(mocker, capsys):
    """Adding a URL that is already in the archive should not add it again."""
    mock_httpx = mocker.patch("archeion.index.models.httpx")
    mock_httpx.head.return_value = Response(status_code=200, headers={"content-type": "text/html"}, content="")
    links_1 = add_links("https://example.com")
    links_2 = add_links("https://example.com")
    captured = capsys.readouterr()
    output = [line.rstrip() for line in captured.out.splitlines()]
    assert output == [
        "ℹ Parsing input",
        "  ℹ Parsed 1 URLs from input",
        "  ℹ Found 1 new URLs not already in index",
        "ℹ Parsing input",
        "  ℹ Parsed 1 URLs from input",
        "  ℹ Found 0 new URLs not already in index",
    ]
    assert len(links_1) == 1
    assert len(links_2) == 0
    assert Link.objects.count() == 1
    assert Artifact.objects.count() == archiver_count


def test_add_links_index_only(mocker, capsys):
    """Adding index-only links do not create an Artifact."""
    mock_httpx = mocker.patch("archeion.index.models.httpx")
    mock_httpx.head.return_value = Response(status_code=200, headers={"content-type": "text/html"}, content="")
    links = add_links("https://example.com", index_only=True)
    captured = capsys.readouterr()
    output = [line.rstrip() for line in captured.out.splitlines()]
    assert output == [
        "ℹ Parsing input",
        "  ℹ Parsed 1 URLs from input",
        "  ℹ Found 1 new URLs not already in index",
    ]
    assert len(links) == 1
    assert Link.objects.count() == 1
    assert Artifact.objects.count() == 0


def test_add_links_specific_archiver(mocker, capsys):
    """Adding index-only links do not create an Artifact."""
    mock_httpx = mocker.patch("archeion.index.models.httpx")
    mock_httpx.head.return_value = Response(status_code=200, headers={"content-type": "text/html"}, content="")
    links = add_links("https://example.com", archiver_names=["DOM"])
    captured = capsys.readouterr()
    output = [line.rstrip() for line in captured.out.splitlines()]
    assert output == [
        "ℹ Parsing input",
        "  ℹ Parsed 1 URLs from input",
        "  ℹ Found 1 new URLs not already in index",
    ]
    assert len(links) == 1
    assert Link.objects.count() == 1
    assert Artifact.objects.count() == 1
