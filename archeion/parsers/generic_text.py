"""Parser for URLs in text files."""

import os
import re
from pathlib import Path
from typing import List

from archeion.parsers import str_is_path
from archeion.utils import extract_webloc_url

URL_REGEX = re.compile(
    r"(?=("
    r"http[s]?://"  # start matching from allowed schemes
    r"(?:[a-zA-Z]|[0-9]"  # followed by allowed alphanum characters
    r"|[$-_@.&+]|[!*\(\),]"  # or allowed symbols
    r"|(?:%[0-9a-fA-F][0-9a-fA-F]))"  # or allowed unicode bytes
    r'[^\]\[\(\)<>"\'\s]+'  # stop parsing at these symbols
    r"))",
    re.IGNORECASE,
)


def parse_links_from_directory(dir_path: Path) -> List[str]:
    """Parse URLs from a directory."""
    links = []
    for root, _dirs, files in os.walk(dir_path):
        for file in files:
            file_path = Path(f"{root}/{file}")
            links.extend(parse_links_from_path(file_path))
    return links


def parse_links_from_path(filepath: Path) -> List[str]:
    """Parse URLs from each line in a text file."""
    if filepath.is_dir():
        return parse_links_from_directory(filepath)
    if filepath.suffix == ".webloc":
        return [extract_webloc_url(filepath)]
    elif filepath.suffix != ".txt":
        return []

    lines = filepath.read_text().splitlines()
    links = []

    for line in lines:
        links.extend(re.findall(URL_REGEX, line))

    return links


def parse_text(value: str) -> List[str]:
    """Parse raw URLs from each line in a string or text file."""
    if str_is_path(value):
        return parse_links_from_path(Path(value))

    lines = value.splitlines()
    links = []

    for line in lines:
        links.extend(re.findall(URL_REGEX, line))

    return links
