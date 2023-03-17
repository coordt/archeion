"""Process HTML html_metadata data."""


def process_html_metadata(item: dict) -> dict:
    """
    Process HTML html_metadata data.

    Args:
        item: All the key-value pairs from the HTML html_metadata tags

    Returns:
        Necessary key-value pairs
    """
    output = {
        "headline": item.get("title"),
        "description": item.get("description"),
        "keywords": None,
    }
    if "keywords" in item:
        output["keywords"] = {key.strip() for key in item.get("keywords", "").split(",")}
    if "author" in item:
        output["author"] = [
            {
                "type": "https://schema.org/Person",
                "name": item.get("author"),
            }
        ]
    return output
