"""Post-process links."""
# Metadata
# convert to Markdown html2text https://github.com/Alir3z4/html2text/blob/master/docs/usage.md
# Summary: https://platform.openai.com/playground/p/default-chat?model=text-davinci-003
from typing import List, Optional

from django.db.models import QuerySet

from archeion.index.models import Artifact, ArtifactStatus, Link
from archeion.logging import info


def get_links_with_dom() -> QuerySet:
    """Get all Links with pending status."""
    return (
        Link.objects.filter(artifacts__status=ArtifactStatus.SUCCEEDED, artifacts__plugin_name="dom")
        .prefetch_related("artifacts")
        .order_by("-created_at")
    )


def post_process_links(links: Optional[List[Link]] = None, overwrite: bool = False) -> None:
    """Post process archived links."""
    if links is None:
        links = get_links_with_dom()
        info("Post-processing links with DOM artifacts...")
    else:
        info(f"Post-processing {len(links)} links...")

    for link in links:
        info(f"Post-processing link {link.url}...")

        post_process(link, overwrite)


def post_process(link: Link, overwrite: bool = False) -> None:
    """Given a link, generate post_processors from the DOM artifact."""
    from archeion.index.storage import get_artifact_storage
    from archeion.post_processors.html import save_html_metadata
    from archeion.post_processors.markdown import convert_to_markdown

    storage = get_artifact_storage()

    try:
        dom_artifact = link.artifacts.get(plugin_name="DOM")
        dom_content = storage.open(dom_artifact.archive_output_path, "r").read()

        save_html_metadata(dom_content, link, overwrite)

        # Convert to Markdown
        convert_to_markdown(dom_content, link, overwrite)

        # Summarize
    except Artifact.DoesNotExist:
        return
