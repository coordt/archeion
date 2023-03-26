"""Generic utilities that don't fit anywhere else."""
import contextlib
import os
import re
from pathlib import Path
from typing import Any, Generator, Optional, Union

from django.conf import settings
from django.core.files.storage import Storage
from django.core.serializers.json import DjangoJSONEncoder
from slugify import slugify

from archeion.stopwords import STOPWORDS


@contextlib.contextmanager
def temp_cd(path: Union[str, Path]) -> Generator:
    """
    Temporarily change the current working directory to the given path.

    Example:
        >>> with temp_cd('/tmp/foo'):
        >>>     ...

    Args:
        path: The path to change the current working directory to.

    Yields:
        None
    """
    d = os.getcwd()

    # This could raise an exception, but it's probably
    # best to let it propagate and let the caller
    # deal with it, since they requested x
    os.chdir(path)

    try:
        yield

    finally:
        # This could also raise an exception, but you *really*
        # aren't equipped to figure out what went wrong if the
        # old working directory can't be restored.
        os.chdir(d)


def model_slugify(value: str) -> str:
    """
    Convert a string to a "slugified" string.

    A slug is a string without spaces or special characters.

    Args:
        value: The string to slugify

    Returns:
        The "slugified" string
    """
    return slugify(value, stopwords=STOPWORDS)


def get_dir_size(storage: Storage, path: str, recursive: bool = True, pattern: Optional[str] = None) -> int:
    """
    Get the total disk size of a given directory.

    Args:
        storage: The Django storage class to use for file access
        path: The path to calculate
        recursive: Whether to calculate the size of all subdirectories
        pattern: A regex pattern to match the files to calculate the size of

    Returns:
        The number of bytes calculated
    """
    num_bytes = 0
    if not storage.exists(path):
        return 0

    for dirs, files in storage.listdir(path):
        for f in files:
            if pattern and not re.search(pattern, f):
                continue
            num_bytes += storage.size(os.path.join(path, f))

        if recursive:
            for d in dirs:
                num_bytes += get_dir_size(storage, os.path.join(path, d), recursive=recursive, pattern=pattern)
    return num_bytes


def normalize_url(url: str) -> str:
    """
    Normalize a URL to avoid potential duplications.

    - remove username/password
    - remove some query string parameters
    - remove fragment
    - remove port if it is redundant (http & 80, https & 443)

    Args:
        url: The URL to normalize

    Returns:
        The normalized URL
    """
    from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

    from w3lib.url import canonicalize_url

    cannonical_url = canonicalize_url(url)
    url_bits = urlparse(cannonical_url.strip())
    url_dict = {
        "scheme": url_bits.scheme,
        "netloc": url_bits.netloc,
        "path": url_bits.path,
        "params": url_bits.params,
        "query": url_bits.query,
        "fragment": "",
    }

    # Strip out username/password and remove redundant port information
    if url_bits.scheme == "http" and url_bits.port in [80, None]:
        url_dict["netloc"] = url_bits.hostname
    elif url_bits.scheme == "https" and url_bits.port in [443, None]:
        url_dict["netloc"] = url_bits.hostname
    elif url_bits.port:
        url_dict["netloc"] = f"{url_bits.hostname}:{url_bits.port}"

    query_string = parse_qsl(url_bits.query)
    new_qs = sorted(
        ((key, val) for key, val in query_string if key.lower() not in settings.STRIPPABLE_QUERY_PARAMS),
        key=lambda x: x[0],
    )
    url_dict["query"] = urlencode(new_qs)

    return urlunparse(tuple(url_dict.values()))


class IterableEncoder(DjangoJSONEncoder):
    """
    A custom encoder that sorts list items.
    """

    def default(self, obj: Any) -> Any:
        """Check for iterables and sort them."""
        try:
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return sorted(iterable)
        # Let the base class default method raise the TypeError
        return DjangoJSONEncoder.default(self, obj)


def ensure_list(item: Any) -> list:
    """Ensure that the item is a list by making it one if it isn't."""
    return list(item) if isinstance(item, (list, tuple)) else [item]
