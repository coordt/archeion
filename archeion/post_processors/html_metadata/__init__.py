"""Gather and normalize HTML html_metadata."""
from typing import Any, Dict, List, Optional

import logging
from collections import ChainMap
from datetime import datetime, timezone

from archeion.post_processors.html_metadata.github import parse_gh_tags
from archeion.post_processors.html_metadata.html import process_html_metadata
from archeion.post_processors.html_metadata.jsonld import parse_jsonld_data
from archeion.post_processors.html_metadata.microdata import process_microdata_data
from archeion.post_processors.html_metadata.opengraph import process_opengraph_data
from archeion.post_processors.html_metadata.twitter import process_twitter_data

logger = logging.getLogger(__name__)


class Normalizer:
    """
    Normalize html_metadata from a big messy pile of html_metadata.

    The order of priority:

    - json-ld
    - html
    - opengraph
    - twitter
    - microdata
    - microformat
    - github
    """

    data: dict
    """The html_metadata extracted from an HTML document."""

    def __init__(self, data, default_source: Optional[str] = None):
        self.data = data
        self.default_source = default_source
        self.lookup = ChainMap(
            self._parse_jsonld(),
            self._parse_html(),
            self._parse_opengraph(),
            self._parse_twitter(),
            self._parse_microdata(),
            self.data["github"],
        )
        logger.info(f"raw html_metadata: {self.lookup.maps}")

    def _parse_jsonld(self) -> dict:
        """
        Parse JSON-LD data into a dict.

        Used in a :class:`~.ChainMap` for looking up key/value pairs

        Returns:
            The extracted key/value pairs. Only keys that have values are included.
        """
        data: List[dict] = self.data.get("json-ld", [])
        return parse_jsonld_data(data) if data else {}

    def _parse_html(self) -> dict:
        """
        Parse normal HTML meta tags into a dict.

        Returns:
            The extracted key/value pairs. Only keys that have values are included.
        """
        data = self.data.get("html", [])
        if not data:
            return {}

        output = process_html_metadata(data[0])
        return {key: val for key, val in output.items() if val}

    def _parse_opengraph(self) -> dict:
        """
        Parse normal HTML meta tags into a dict.

        Returns:
            The extracted key/value pairs. Only keys that have values are included.
        """
        data = self.data.get("opengraph", [])
        if not data:
            return {}

        output = process_opengraph_data(data[0])
        return {key: val for key, val in output.items() if val}

    def _parse_twitter(self) -> dict:
        """
        Parse Twitter meta tags into a dict.

        Returns:
            The extracted key/value pairs. Only keys that have values are included.
        """
        data = self.data.get("twitter", [])
        if not data:
            return {}

        output = process_twitter_data(data[0])
        return {key: val for key, val in output.items() if val}

    def _parse_microdata(self) -> dict:
        """
        Parse microdata into a dict.

        Most of this parsing is based on YouTube microdata. Other examples are
        required for a more robust parsing.

        Returns:
            The extracted key/value pairs. Only keys that have values are included.
        """
        data = self.data.get("microdata", [])
        if not data:
            return {}

        output = process_microdata_data(data[0])
        return {key: val for key, val in output.items() if val}

    def normalized_metadata(self) -> dict:
        """
        Return the dict with the extracted metadata.

        Returns:
            The html_metadata in a dataclass
        """
        return {
            "type": self.type,
            "headline": self.headline,
            "description": self.description,
            "author": self.author,
            "publisher": self.publisher,
            "keywords": self.keywords,
            "datePublished": self.datePublished,
            "source": self.source,
            "sourceEncodingFormat": self.sourceEncodingFormat,
            "encodingFormat": self.sourceEncodingFormat,
        }

    @property
    def type(self) -> str:
        """Figure out the type from all the html_metadata."""
        return self.lookup.get("type", "https://schema.org/CreativeWork")

    @property
    def headline(self) -> Optional[str]:
        """Figure out the headline from all the html_metadata."""
        return self.lookup.get("headline")

    @property
    def description(self) -> Optional[str]:
        """Figure out the description from all the html_metadata."""
        return self.lookup.get("description")

    @property
    def author(self) -> Optional[list]:
        """Figure out the author from all the html_metadata."""
        return self.lookup.get("author")

    @property
    def publisher(self) -> Optional[list]:
        """Figure out the publisher from all the html_metadata."""
        return self.lookup.get("publisher")

    @property
    def keywords(self) -> set:
        """Combine and deduplicate the keywords from all the html_metadata."""
        return set().union(*[m.get("keywords", set()) for m in self.lookup.maps])

    @property
    def datePublished(self) -> datetime:
        """Figure out the keywords from all the html_metadata."""
        return self.lookup.get("datePublished", datetime.now(tz=timezone.utc))

    @property
    def source(self) -> Optional[str]:
        """Figure out the source from all the html_metadata."""
        return self.lookup.get("source", self.default_source)

    @property
    def sourceEncodingFormat(self) -> str:
        """Figure out the keywords from all the html_metadata."""
        return self.lookup.get("sourceEncodingFormat", "text/html")


def extract_metadata(page_source: str, url: Optional[str] = None) -> dict:
    """
    Aggregate all the test_metadata from a parsed HTML file.

    Args:
        page_source: The raw HTML source for a web page
        url: The URL for the page

    Returns:
        The extracted html_metadata
    """
    from collections import defaultdict

    import extruct
    from bs4 import BeautifulSoup

    data = extruct.extract(page_source, base_url=url)

    soup = BeautifulSoup(page_source, "html.parser")
    meta_groups: Dict[str, Dict[str, Any]] = defaultdict(dict)
    title = soup.title
    meta_groups["html"]["title"] = title.text.strip() if title else None

    for tag in soup.find_all("meta"):
        name = tag.attrs.get("property", tag.attrs.get("name"))
        if name is None:
            continue
        group, tag_name = name.split(":", maxsplit=1) if ":" in name else ("html", name)
        meta_groups[group][tag_name] = tag.attrs.get("content")

    if "html" in meta_groups:
        data["html"] = [meta_groups["html"]]
    if "twitter" in meta_groups:
        data["twitter"] = [meta_groups["twitter"]]
    data["github"] = {"keywords": parse_gh_tags(soup) or []}
    return data
