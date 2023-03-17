"""Parser for RSS and Atom feeds."""

from typing import List


def parse_generic_feed(value: str) -> List[str]:
    """Parse RSS and Atom files or URLs into links."""
    import feedparser

    feed = feedparser.parse(value)
    return [item.link.strip() for item in feed.entries]
