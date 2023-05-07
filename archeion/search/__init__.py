"""Search interface for Archeion."""
from importlib import import_module
from typing import List, Protocol

from django.conf import settings
from django.db.models import QuerySet

from archeion.index.models import Artifact, Link
from archeion.logging import error


class SearchBackend(Protocol):
    """The minimum expected interface for a search backend."""

    def __init__(self, config: dict):
        ...

    def index_link(self, link_id: str, tags: List[str]) -> None:
        """
        Index the tags for the link_id.
        """
        ...

    def index_artifact(self, artifact_id: str, link_id: str, content: str) -> None:
        """Index the content for an artifact/link combination."""
        ...

    def search(self, query: str) -> List[str]:
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


def index_link(link: Link) -> None:
    """Index the attributes of the given Link."""
    search_backend = get_search_backend()
    search_backend.index_link(link.id, link.tags)


def index_artifact(artifact: Artifact, content: str) -> None:
    """Index the content of the given Artifact."""
    search_backend = get_search_backend()
    search_backend.index_artifact(artifact_id=artifact.id, link_id=artifact.link_id, content=content)


def search(query: str) -> QuerySet:
    """Search the index and return a QuerySet of Link IDs."""
    search_backend = get_search_backend()
    link_ids = search_backend.search(query)
    if link_ids:
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
