"""Search interface for Archeion."""

from importlib import import_module
from typing import List, Protocol, Tuple

from django.conf import settings
from django.db.models import QuerySet

from archeion.index.models import Link
from archeion.logging import error

SearchResult = Tuple[str, float]


class SearchBackend(Protocol):
    """The minimum expected interface for a search backend."""

    def __init__(self, config: dict): ...

    def index(self, link_id: str, content: str) -> None:
        """Index the content for a link."""
        ...

    def search(self, query: str, limit: int = 1000) -> List[SearchResult]:
        """
        Return a list of Link IDs of all the results for the given query.
        """
        ...


def get_search_backend() -> SearchBackend:
    """Import and return the search backend class."""
    module, class_name = settings.SEARCH_CONFIG.backend.rsplit(".", 1)
    try:
        klass = getattr(import_module(module), class_name)
        return klass(settings.SEARCH_CONFIG)
    except (ImportError, AttributeError) as e:
        error(f"Unable to load search backend {class_name}: {e}")
        raise ImportError(f"Unable to load search backend {class_name}: {e}") from e


def index(link_id: str, content: str) -> None:
    """Index the content of the given Artifact."""
    # TODO: Allow updating the index
    search_backend = get_search_backend()
    search_backend.index(link_id, content)


def delete(link_id: str) -> None:
    """Delete the content of the given Link."""
    # TODO: implement the deleting process
    pass


def search(query: str) -> QuerySet:
    """Search the index and return a QuerySet of Link IDs."""
    search_backend = get_search_backend()
    search_results = search_backend.search(query)
    if search_results:
        # TODO: Actually sort by rank
        link_ids = [link_id for link_id, _ in search_results]
        return Link.objects.filter(pk__in=link_ids)

    return Link.objects.none()


# def index_links(
#     links: Union[List[Link], None],
# ):
#     if not links:
#         return
#
#     from .utils import get_indexable_content, log_index_started
#     from core.models import ArchiveResult, Snapshot
#
#     for link in links:
#         snap = Snapshot.objects.filter(url=link.url).first()
#         if snap:
#             results = ArchiveResult.objects.indexable().filter(snapshot=snap)
#             log_index_started(link.url)
#             try:
#                 texts = get_indexable_content(results)
#             except Exception as err:
#                 stderr()
#                 stderr(
#                     f"[X] An Exception ocurred reading the indexable content={err}:",
#                     color="red",
#                 )
#             else:
#                 write_search_index(link, texts, out_dir=out_dir)
