"""Tests for the URL list link parser."""

from pathlib import Path

import pytest
from pytest import param

from archeion.parsers.generic_text import parse_links_from_path


@pytest.mark.parametrize(
    "file_path, expected_links",
    [
        param(
            "url-list.txt",
            [
                "https://farrell-turner.info/",
                "https://cooper-christian.com/#fragment",
                "https://dalton.com/?q=1&b=56",
                "http://cox.com/tag/posts/search.html",
                "https://gross-melton.com/",
                "https://www.miller-mckenzie.org/author/",
                "http://dodson-pham.com/category.html",
                "https://www.berg-cruz.com/list/tags/app/post.html",
            ],
            id="full-path-url_list.txt",
        )
    ],
)
def test_parse_txt_file_filepath(file_path: str, expected_links: list, fixture_dir: Path):
    """If a file path is passed as the string, it should read it and parse it."""
    fullpath = fixture_dir.joinpath(file_path)
    urls = parse_links_from_path(fullpath)
    assert isinstance(urls, list)
    assert set(urls) == set(expected_links)
