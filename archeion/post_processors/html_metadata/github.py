"""Pulling tags from github pages."""

from bs4 import BeautifulSoup


def parse_gh_tags(soup: BeautifulSoup) -> set:
    """
    Parse tags from a GitHub repository page.

    Args:
        soup: The Beautiful Soup-parsed object

    Returns:
        A set of string tags. Might be an empty set if no tags exist.
    """
    return {i.string.strip() for i in soup.find_all(attrs={"class": "topic-tag"})}
