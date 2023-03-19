"""Modified from https://github.com/scrapinghub/extruct ."""
from typing import Any, Iterable, List, Optional, Protocol, Tuple

import logging

from extruct.dublincore import DublinCoreExtractor
from extruct.jsonld import JsonLdExtractor
from extruct.microformat import MicroformatExtractor
from extruct.opengraph import OpenGraphExtractor
from extruct.rdfa import RDFaExtractor
from extruct.w3cmicrodata import MicrodataExtractor
from extruct.xmldom import XmlDomHTMLParser
from lxml import html  # nosec B410

logger = logging.getLogger(__name__)
SYNTAXES = ("microdata", "opengraph", "json-ld", "microformat", "rdfa", "dublincore")


class Extractor(Protocol):
    """
    Extracts metadata from an HTML document.
    """

    def __call__(self, *args, **kwargs) -> dict:
        """
        Extracts metadata from an HTML document.
        """
        ...


def extract(
    htmlstring: str,
    base_url: Optional[str] = None,
    syntaxes: Iterable = SYNTAXES,
):
    """
    Extracts metadata from an HTML document.

    Args:
        htmlstring: string with valid html document;
        base_url: base url of the html document
        syntaxes: list of syntaxes to extract

    Raises:
        ValueError: if syntaxes is not an iterable

    Returns:
        A dictionary with extracted metadata.
    """
    if any(v not in SYNTAXES for v in syntaxes):
        raise ValueError(f"`syntaxes` must be a list with any or all (default) of these values: {SYNTAXES}")

    body = htmlstring.strip().replace("\x00", "").encode("utf8") or b"<html/>"
    parser = XmlDomHTMLParser(recover=True, encoding="utf8")
    tree = html.document_fromstring(body, parser=parser, base_url=base_url)  # nosec B320
    processors = get_processors(syntaxes, htmlstring, tree)

    return {syntax: list(extractor(document, base_url=base_url)) for syntax, extractor, document in processors}


def get_processors(syntaxes: Iterable, htmlstring: str, tree) -> List[Tuple[str, Extractor, Any]]:
    """
    Returns a list of tuples (syntax, extractor, document).

    Args:
        syntaxes: The list of syntaxes to extract.
        htmlstring: A string with valid html document.
        tree: The html tree.

    Returns:
        The list of processors
    """
    processors = []
    if "microdata" in syntaxes:
        processors.append(("microdata", MicrodataExtractor().extract_items, tree))
    if "json-ld" in syntaxes:
        processors.append(
            (
                "json-ld",
                JsonLdExtractor().extract_items,
                tree,
            )
        )
    if "opengraph" in syntaxes:
        processors.append(("opengraph", OpenGraphExtractor().extract_items, tree))
    if "microformat" in syntaxes:
        processors.append(("microformat", MicroformatExtractor().extract_items, htmlstring))
    if "rdfa" in syntaxes:
        processors.append(
            (
                "rdfa",
                RDFaExtractor().extract_items,
                tree,
            )
        )
    if "dublincore" in syntaxes:
        processors.append(
            (
                "dublincore",
                DublinCoreExtractor().extract_items,
                tree,
            )
        )
    return processors
