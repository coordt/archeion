"""Methods for parsing links from input sources."""
from pathlib import Path
from typing import Callable, List

from archeion.logging import error

Parser = Callable[[str], List[str]]


def get_parsers() -> List[Parser]:
    """Return a list of the instantiated parsers from configuration."""
    import importlib

    from django.conf import settings

    parsers = []

    for parser in settings.LINK_PARSERS:
        module, func_name = parser.rsplit(".", 1)
        try:
            parser_func = getattr(importlib.import_module(module), func_name)
            parsers.append(parser_func)
        except (ImportError, AttributeError) as e:
            error(f"Unable to load parser {func_name}: {e}")

    return parsers


def parse_input(value: str) -> List[str]:
    """Parse an input string into a list of links."""
    if not value:
        return []

    parsers = get_parsers()

    for parser in parsers:
        links = parser(value)
        if links:
            return links

    return []


def str_is_path(value: str) -> bool:
    """Return True if the value is a path to a file or directory."""
    if value.startswith("file://"):
        return True

    return False if len(value) > 255 else bool(Path(value).exists())


def str_is_url(value: str) -> bool:
    """Return True if the value is a URL."""
    stripped_val = value.strip()
    if "\n" in stripped_val:
        return False
    return value.startswith("http://") or value.startswith("https://")


def str_is_html(value: str) -> bool:
    """Return True if the value is an HTML documentL."""
    import re

    stripped_val = value.strip()

    return re.match("<!doctype html", stripped_val, re.IGNORECASE) is not None


def str_is_rss(value: str) -> bool:
    """Return True if the value is an RSS feed."""
    stripped_val = value.strip()

    return "<rss" in stripped_val


def str_is_atom(value: str) -> bool:
    """Return True if the value is an Atom feed."""
    stripped_val = value.strip()

    return "<feed" in stripped_val
