"""Tests for the generic HTML link parser."""

from pathlib import Path

import pytest
from pytest import param

from archeion.parsers.generic_html import parse_html_links


@pytest.mark.parametrize(
    "file_path, expected_links",
    [
        param(
            "example.com.html",
            ["http://127.0.0.1:8080/static/iana.org.html"],
            id="example.com.html",
        ),
        param(
            "blog_with_base_tag.html",
            [
                "https://getbootstrap.com/docs/5.3/examples/blog/#top",
                "https://getbootstrap.com/2020/apr/",
                "https://getbootstrap.com/2020/aug/",
                "https://getbootstrap.com/2020/dec/",
                "https://getbootstrap.com/2020/jul/",
                "https://getbootstrap.com/2020/jun/",
                "https://getbootstrap.com/2020/may/",
                "https://getbootstrap.com/2020/nov/",
                "https://getbootstrap.com/2020/oct/",
                "https://getbootstrap.com/2020/sep/",
                "https://getbootstrap.com/2021/feb/",
                "https://getbootstrap.com/2021/jan/",
                "https://getbootstrap.com/2021/mar/",
                "https://getbootstrap.com/article1.html",
                "https://getbootstrap.com/article2.html",
                "https://getbootstrap.com/article3.html",
                "https://getbootstrap.com/authors/chris.html",
                "https://getbootstrap.com/authors/jacob.html",
                "https://getbootstrap.com/authors/mark.html",
                "https://getbootstrap.com/business/",
                "https://getbootstrap.com/culture/",
                "https://getbootstrap.com/design/",
                "https://getbootstrap.com/health/",
                "https://getbootstrap.com/large/",
                "https://getbootstrap.com/older/",
                "https://getbootstrap.com/opinion/",
                "https://getbootstrap.com/politics/",
                "https://getbootstrap.com/science/",
                "https://getbootstrap.com/search/",
                "https://getbootstrap.com/signup/",
                "https://getbootstrap.com/style/",
                "https://getbootstrap.com/subscribe/",
                "https://getbootstrap.com/tech/",
                "https://getbootstrap.com/travel/",
                "https://getbootstrap.com/us/",
                "https://getbootstrap.com/world/",
                "https://developer.mozilla.org/en-US/docs/Web/HTML/Element",
                "https://facebook.com/",
                "https://getbootstrap.com/",
                "https://github.com/",
                "https://twitter.com/",
                "https://twitter.com/mdo",
            ],
            id="blog_with_base_tag.html",
        ),
        param(
            "blog.html",
            [
                "#top",
                "/2020/apr/",
                "/2020/aug/",
                "/2020/dec/",
                "/2020/jul/",
                "/2020/jun/",
                "/2020/may/",
                "/2020/nov/",
                "/2020/oct/",
                "/2020/sep/",
                "/2021/feb/",
                "/2021/jan/",
                "/2021/mar/",
                "/article1.html",
                "/article2.html",
                "/article3.html",
                "/authors/chris.html",
                "/authors/jacob.html",
                "/authors/mark.html",
                "/business/",
                "/culture/",
                "/design/",
                "/health/",
                "/large/",
                "/older/",
                "/opinion/",
                "/politics/",
                "/science/",
                "/search/",
                "/signup/",
                "/style/",
                "/subscribe/",
                "/tech/",
                "/travel/",
                "/us/",
                "/world/",
                "https://developer.mozilla.org/en-US/docs/Web/HTML/Element",
                "https://facebook.com/",
                "https://getbootstrap.com/",
                "https://github.com/",
                "https://twitter.com/",
                "https://twitter.com/mdo",
            ],
            id="blog.html",
        ),
        param(
            "malformed.html",
            [],
            id="malformed.html",
        ),
        param(
            "bookmark-export.html",
            [
                "http://twitter.com",
                "http://www.daveeddy.com",
                "http://www.perfume-global.com/",
                "http://www.tekzoned.com",
                "http://www.youtube.com",
                "https://github.com",
            ],
            id="bookmark-export.html",
        ),
    ],
)
def test_parse_html_links(file_path: str, expected_links: list, fixture_dir: Path):
    """The parser should return a list of links."""
    html = (fixture_dir / file_path).read_text()
    found_links = parse_html_links(html)
    assert isinstance(found_links, list)
    assert set(found_links) == set(expected_links)
