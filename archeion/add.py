"""Add a link to the archive."""

from typing import List, Optional

from archeion.archivers import get_default_archivers
from archeion.index.models import Link
from archeion.logging import info
from archeion.utils import normalize_url


def add_links(input_: str, index_only: bool = False, archiver_names: Optional[List[str]] = None) -> List[Link]:
    """
    Add a new URL or list of URLs to your archive.

    Args:
        input_: The value to parse for URLs.
        index_only: Only add the URL to the index, do not add any archivers
        archiver_names: A list of archivers to use. If not provided, all configured archivers

    Returns:
        A list of Link objects.
    """
    from archeion.parsers import parse_input

    info("Parsing input")
    urls = parse_input(input_)
    info(f"Parsed {len(urls)} URLs from input", left_indent=2)

    if not urls:
        return []

    duplicate_urls: List[str] = []
    links_to_archive: List[Link] = []

    default_archivers = get_default_archivers()

    if index_only:
        archivers = []
    elif archiver_names is None:
        archivers = default_archivers
    else:
        archivers = [archiver for archiver in default_archivers if archiver.plugin_name in archiver_names]

    for url in urls:
        normalized_url = normalize_url(url)
        if Link.objects.filter(url=normalized_url).exists():
            duplicate_urls.append(normalized_url)
        else:
            link = Link.objects.create(url=normalized_url)
            links_to_archive.append(link)

            if index_only:
                continue

            for archiver in archivers:
                link.artifacts.create(plugin_name=archiver.plugin_name)

    info(f"Found {len(links_to_archive)} new URLs not already in index", left_indent=2)
    return links_to_archive
