"""Tests for the parser's __init__.py."""

from archeion.parsers import (
    get_parsers,
    parse_input,
    str_is_atom,
    str_is_html,
    str_is_path,
    str_is_rss,
    str_is_url,
)


def test_get_parsers():
    """Test the get_parsers function."""
    parsers = get_parsers()
    assert len(parsers) > 0
    assert all(callable(parser) for parser in parsers)


def test_get_parsers_missing_parser(settings, capsys):
    """Test the get_parsers function with a missing parser."""
    settings.LINK_PARSERS.append("missing.parser")
    parsers = get_parsers()
    captured = capsys.readouterr()
    assert "Unable to load parser" in captured.out
    assert len(parsers) > 0


def test_str_is_path(tmp_path):
    """Test the str_is_path function."""
    assert str_is_path(f"file://{tmp_path}")
    assert str_is_path(str(tmp_path))
    assert not str_is_path("x" * 256)


def test_str_is_url():
    """Test the str_is_url function."""
    assert str_is_url("http://example.com")
    assert str_is_url("https://example.com")
    assert str_is_url("http://example.com               ")
    assert str_is_url("http://example.com\n")
    assert not str_is_url("example.com")
    assert not str_is_url("http://example.com\nexample.com")


def test_str_is_html(fixture_dir):
    """Test the str_is_html function."""
    assert str_is_html(fixture_dir.joinpath("blog.html").read_text())
    assert not str_is_html(fixture_dir.joinpath("url-list.txt").read_text())


def test_str_is_atom(fixture_dir):
    """Test the str_is_atom function."""
    assert str_is_atom(fixture_dir.joinpath("example.atom.xml").read_text())
    assert not str_is_atom(fixture_dir.joinpath("url-list.txt").read_text())


def test_str_is_rss(fixture_dir):
    """Test the str_is_rss function."""
    assert str_is_rss(fixture_dir.joinpath("example.rss.xml").read_text())
    assert not str_is_rss(fixture_dir.joinpath("url-list.txt").read_text())
