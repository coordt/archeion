"""Tests for parsing links from an RSS feed."""

from archeion.parsers.generic_feed import parse_generic_feed

EXPECTED_LINKS = {
    "http://www.feedforall.com/banks.htm",
    "http://www.feedforall.com/computer-service.htm",
    "http://www.feedforall.com/government.htm",
    "http://www.feedforall.com/law-enforcement.htm",
    "http://www.feedforall.com/politics.htm",
    "http://www.feedforall.com/real-estate.htm",
    "http://www.feedforall.com/restaurant.htm",
    "http://www.feedforall.com/schools.htm",
    "http://www.feedforall.com/weather.htm",
}


def test_parse_rss_feed_string(fixture_dir):
    """Test parsing an RSS feed string."""
    rss = fixture_dir.joinpath("example.rss.xml").read_text()
    links = parse_generic_feed(rss)
    assert set(links) == EXPECTED_LINKS


def test_parse_rss_feed_filepath(fixture_dir):
    """Test parsing an RSS feed string."""
    rsspath = fixture_dir.joinpath("example.rss.xml")
    links = parse_generic_feed(str(rsspath))
    assert set(links) == EXPECTED_LINKS


def test_parse_rss_feed_url(fixture_dir, httpserver):
    """Test parsing an RSS feed string."""
    rss = fixture_dir.joinpath("example.rss.xml").read_text()
    httpserver.serve_content(rss, headers={"Content-Type": "application/rss+xml;charset=UTF-8"})
    links = parse_generic_feed(httpserver.url)
    assert set(links) == EXPECTED_LINKS
