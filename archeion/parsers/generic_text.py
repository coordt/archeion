"""Parser for URLs in text files."""

from typing import List

import re
from pathlib import Path

from archeion.parsers import str_is_path

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


def parse_txt_file(value: str) -> List[str]:
    """Parse raw URLs from each line in a string or text file."""
    if str_is_path(value):
        lines = Path(value).read_text().splitlines()
    else:
        lines = value.splitlines()

    links = []

    for line in lines:
        links.extend(re.findall(URL_REGEX, line))

    return links
