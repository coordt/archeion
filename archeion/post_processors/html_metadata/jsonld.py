"""JSON-LD parsing."""
import json
from collections import ChainMap
from typing import List, Optional

import dateutil.parser
import networkx as nx
from django.conf import settings

from archeion.dependency import run_shell
from archeion.logging import error
from archeion.utils import ensure_list

jsonld_type_blacklist = ("ReadAction", "BreadcrumbList", "ListItem", "SearchAction")


def contextify(context: str, value: str) -> str:
    """
    Prepend context URL to the value, if value is not a URL.

    Args:
        context: The URL of the context
        value: The ID of the item

    Returns:
        A fully qualified URL
    """
    if not value.startswith("http"):
        if context.endswith("#"):
            return f"{context}{value}"
        else:
            return f"{context.rstrip('/')}/{value}"
    return value


def parse_jsonld_data(data: List[dict]) -> dict:  # noqa: C901
    """
    Parse JSON-LD data from :mod:`extruct`.

    Args:
        data: A list of zero or more ``dict``s of JSON-LD data

    Returns:
        The extracted key-value pairs
    """
    output: dict = {
        "type": [],
        "headline": [],
        "description": [],
        "author": [],
        "publisher": [],
        "keywords": set(),
        "datePublished": [],
        "source": [],
        "sourceEncodingFormat": "text/html",
    }

    # build a dict of id/url -> object for easy dereferencing
    # pick one of the elements that is likely the content
    # embed the objects for publisher and author(s)

    indexes = [index_jsonld_obj(item) for item in data]
    master_index = dict(ChainMap(*indexes))
    edge = get_primary_node(master_index)
    items = [edge] if edge else list(master_index.values())
    retval = {}
    for item in items:
        if "url" in item:
            output["source"].append(item.get("url"))
        if "id" in item:
            output["source"].append(item.get("id"))

        if "@context" in item and isinstance(item["@context"], str):
            current_context = item["@context"]
        else:
            current_context = "https://schema.org/"

        if item.get("type", "") in jsonld_type_blacklist:
            continue
        else:
            output["type"] = contextify(current_context, item.get("type", "CreativeWork"))

        if "headline" in item or "name" in item:
            output["headline"].append(item.get("headline", item.get("name")))
        if "description" in item:
            output["description"].append(item.get("description"))

        authors: List[dict] = ensure_list(item.get("author", []))
        output["author"] = contextify_authors(authors, current_context, master_index)

        publishers: List[dict] = ensure_list(item.get("publisher", []))
        output["publisher"] = contextify_publishers(publishers, current_context, master_index)

        if "keywords" in item:
            if isinstance(item["keywords"], (list, tuple)):
                output["keywords"] |= set(item["keywords"])
            else:
                output["keywords"] |= {item["keywords"]}

        if "datePublished" in item:
            output["datePublished"].append(dateutil.parser.isoparse(item["datePublished"]))

        retval = {key: val for key, val in output.items() if val}
        for key in ["datePublished", "type", "headline", "description", "source"]:
            val = retval.get(key, [])
            if len(val) == 1:
                retval[key] = val[0]

    return retval


def contextify_publishers(publishers: list, context_url: str, master_index: dict) -> list:
    """Contextify a list of publishers."""
    output = []
    for publisher in publishers:
        if isinstance(publisher, dict):
            if len(publisher) == 1 and "id" in publisher:
                publisher_ctx = master_index[publisher["id"]]
            else:
                publisher_ctx = publisher.copy()

            if "type" in publisher_ctx:
                publisher_ctx["type"] = contextify(context_url, publisher_ctx["type"])
        else:
            publisher_ctx = str(publisher)

        output.append(publisher_ctx)
    return output


def contextify_authors(authors: list, context_url: str, master_index: dict) -> list:
    """Contextify a list of authors."""
    output = []
    for author in authors:
        if isinstance(author, dict):
            if len(author) == 1 and "id" in author:
                author_ctx = master_index[author["id"]]
            else:
                author_ctx = author.copy()
        else:
            author_ctx = {"type": "Person", "name": str(author)}

        if "type" in author_ctx:
            if isinstance(author_ctx["type"], list):
                author_ctx["type"] = author_ctx["type"][0]

            author_ctx["type"] = contextify(context_url, author_ctx["type"])

        output.append(author_ctx)
    return output


def index_jsonld_obj(data: dict) -> dict:
    """
    Index a normal JSON-LD object.

    Args:
        data: The JSON-LD object

    Returns:
        A map of object id to object
    """
    if "@context" in data and isinstance(data["@context"], str):
        data["@context"] = data["@context"].replace("http://schema.org", "https://schema.org")

    json_ld_data = json.dumps(data)

    results = run_shell("./ld-cli compact --pretty https://schema.org/", cwd=settings.APPS_DIR, input=json_ld_data)
    if results.returncode != 0:
        error(["Failed to compact JSON-LD data:", results.stderr])
    compact_data = json.loads(results.stdout)

    if "@graph" in compact_data:
        return {o["id"]: o for o in compact_data["@graph"]}
    elif "id" in compact_data:
        return {compact_data["id"]: compact_data}
    elif "url" in compact_data:
        return {compact_data["url"]: compact_data}
    elif "type" in compact_data:
        return {f"#{compact_data['type'].lower()}": compact_data}
    else:
        return {}


def get_primary_node(index: dict) -> Optional[dict]:
    """
    Return the primary node (e.g. Article) from the index if it is determinable.

    Args:
        index: All the objects in a JSON-LD context that could be the primary node.

    Returns:
        The last node, if it exists
    """
    if len(index) == 1:
        return list(index.values())[0]

    g = nx.MultiDiGraph()
    g.add_nodes_from(index)
    for _key, val in index.items():
        if "isPartOf" in val:
            if isinstance(val["isPartOf"], str):
                g.add_edge(val["isPartOf"], val["id"])
            elif isinstance(val["isPartOf"], dict):
                g.add_edge(val["isPartOf"]["id"], val["id"])
    out_nodes = [x for x in g.nodes() if g.out_degree(x) == 0 and g.in_degree(x) == 1]

    if len(out_nodes) == 1:
        return index[out_nodes[0]]
    else:
        # If there is 0 or more than 1, we don't know what to do.
        return None
