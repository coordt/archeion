"""Tests for GitHub tag parsing."""
from pathlib import Path

from archeion.post_processors.html_metadata import github

FIXTURE_DIR = Path(__file__).parent.parent / "fixtures" / "html-metadata"


def test_parse_gh_tags():
    """Properly parses tags from a github page."""
    from bs4 import BeautifulSoup

    filepath = FIXTURE_DIR / "github.html"
    soup = BeautifulSoup(filepath.read_text(), features="lxml")
    tags = github.parse_gh_tags(soup)
    expected = {
        "cli",
        "digital-brain",
        "elasticsearch",
        "knowledge",
        "knowledge-base",
        "note-taking",
        "productivity",
        "python",
    }
    assert tags == expected
