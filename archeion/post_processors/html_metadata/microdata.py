"""Microdata proccessing."""

import dateutil.parser


def process_microdata_data(data: dict) -> dict:
    """
    Parse microdata extracted from :mod:`extruct`.

    Args:
        data: A ``dict`` with keys ``type`` and ``properties``

    Returns:
        The extracted key-value pairs
    """
    output = {
        "type": data.get("type"),
        "headline": data.get("properties", {}).get("name"),
        "description": data.get("properties", {}).get("description"),
        "author": [],
        "publisher": [],
        "keywords": set(),
        "datePublished": None,
        "source": data["properties"].get("url"),
        "sourceEncodingFormat": "text/html",
    }

    if "author" in data["properties"]:
        if isinstance(data["properties"]["author"], str):
            output["author"].append(
                {
                    "type": "https://schema.org/Person",
                    "name": data["properties"]["author"],
                }
            )
        elif isinstance(data["properties"]["author"], dict):
            output["author"].append(
                {
                    "type": data["properties"]["author"].get("type", "https://schema.org/Person"),
                    **data["properties"]["author"].get("properties", {}),
                }
            )

    if "datePublished" in data["properties"]:
        output["datePublished"] = dateutil.parser.isoparse(data["properties"]["datePublished"])

    return output
