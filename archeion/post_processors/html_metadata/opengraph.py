"""
Open Graph processing.
"""
from collections import defaultdict

import dateutil
import dateutil.parser
from django.conf import settings


def process_opengraph_data(data: dict) -> dict:  # noqa: C901
    """
    Process Open Graph data as extracted from :mod:`extruct`.

    Args:
        data: A ``dict`` with keys ``namespace`` and ``properties``

    Returns:
        Key-value pairs from the data
    """
    init_output = defaultdict(list)

    for tag, value in data["properties"]:
        if tag not in settings.OG_TAG_MAP:
            continue
        init_output[settings.OG_TAG_MAP[tag]].append(value)

    output = {}
    for key, val in init_output.items():
        if len(val) == 0:
            continue
        elif len(val) == 1:
            output[key] = val[0]
        else:
            output[key] = val

    if "type" in output:
        output["type"] = settings.OG_TYPE_MAP.get(output["type"], "https://schema.org/CreativeWork")
    else:
        output["type"] = "https://schema.org/CreativeWork"

    if "publisher" in output:
        output["publisher"] = [
            {
                "type": "https://schema.org/Organization",
                "name": output["publisher"],
            }
        ]

    if "datePublished" in output:
        output["datePublished"] = dateutil.parser.isoparse(output["datePublished"])

    authors = output.get("author", [])
    if not isinstance(authors, (list, tuple)):
        authors = [authors]

    output["author"] = [{"type": "https://schema.org/Person", "name": name} for name in authors]

    if "keywords" in output:
        if isinstance(output["keywords"], (list, tuple)):
            output["keywords"] = {key.strip() for key in output["keywords"]}
        else:
            output["keywords"] = set(output["keywords"].strip())

    return output
