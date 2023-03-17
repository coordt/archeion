"""Process Twitter html_metadata."""


def process_twitter_data(data: dict) -> dict:
    """
    Process Twitter html_metadata extracted via :mod:`extruct`.

    Args:
        data: A ``dict`` with the key-values of metatags that started with ``twitter:``

    Returns:
        The extracted key-value pairs
    """
    output = {
        "headline": data.get("title"),
        "description": data.get("description"),
        "source": data.get("url"),
    }

    author = data.get("creator", data.get("creator:id"))
    if author:
        output["author"] = [
            {
                "type": "https:schema.org/Person",
                "url": f'https://twitter.com/{author.replace("@", "")}',
            }
        ]

    publisher = data.get("site", data.get("site:id"))
    if publisher:
        output["publisher"] = [
            {
                "type": "https://schema.org/Organization",
                "url": f'https://twitter.com/{publisher.replace("@", "")}',
            }
        ]
    return output
