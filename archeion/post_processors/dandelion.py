"""Parsers for Dandelion."""

from dandelion import DataTXT
from django.conf import settings


def get_dandelion_tags(content: str, content_type: str) -> set:  # pragma: no-cover
    """
    Get tags for a :class:`~.Document`.

    Args:
        content: The content to augment
        content_type: The type of content

    Returns:
        A set all tags from Dandelion
    """
    datatxt = DataTXT(token=settings.DANDELION_TOKEN)

    if content_type == "text/html":
        response = datatxt.nex(html=content, timeout=5)
    else:
        response = datatxt.nex(text=content, timeout=5)

    return {i["title"] for i in response["annotations"]}
