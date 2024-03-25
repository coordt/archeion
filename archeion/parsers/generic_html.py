"""Parse an HTML document for its links."""

from html.parser import HTMLParser
from typing import List, Optional, Tuple
from urllib.parse import urljoin

import w3lib.html


class HrefParser(HTMLParser):
    """Parse an HTML document for its links."""

    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag: str, attrs: Optional[List[Tuple[str, str]]]) -> None:
        """Handle start tag."""
        if tag != "a":
            return

        for attr, value in attrs:
            if attr == "href":
                self.urls.append(value)


def parse_html_links(html: str, root_url: Optional[str] = None) -> List[str]:
    """Parse Generic HTML for href tags and use only the url."""
    root_url = root_url or w3lib.html.get_base_url(html)

    parser = HrefParser()
    parser.feed(html)
    parser.close()

    if root_url:
        return [urljoin(root_url, url) for url in parser.urls]

    return parser.urls
