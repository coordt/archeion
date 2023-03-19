"""Test Archeion utils.py."""
from typing import Any

import datetime
import json

import pytest
from pytest import param

from archeion import utils


@pytest.mark.parametrize(
    "url,expected",
    [
        param(
            "https://myuser:mypass@example.com/path/to/file",
            "https://example.com/path/to/file",
            id="remove-auth-from-url",
        ),
        param(
            "https://example.com/path/to/file?utm_campaign=my_campaign&utm_source=my_source",
            "https://example.com/path/to/file",
            id="remove-tracking-params-from-url",
        ),
        param("https://ExamPle.com/Path/to/file", "https://example.com/Path/to/file", id="standardize-domain-case"),
        param("https://example.com:443/", "https://example.com/", id="remove-port-443-redundancy"),
        param("http://example.com:80/", "http://example.com/", id="remove-port-80-redundancy"),
        param("http://example.com:1234/", "http://example.com:1234/", id="keeps-alternative-port"),
        param("http://example.com/#fragment", "http://example.com/", id="removes-fragment"),
    ],
)
def test_normalize_url(url: str, expected: str):
    """Normalizing a URL should return expected results."""
    assert utils.normalize_url(url) == expected


@pytest.mark.parametrize(
    "data,expected",
    [
        param({"a", "b", "c"}, '["a", "b", "c"]', id="set-of-strings-to-list-of-strings"),
        param(
            datetime.datetime(2023, 3, 18, 12, 34, 56, tzinfo=datetime.timezone.utc),
            '"2023-03-18T12:34:56Z"',
            id="datetime-to-string",
        ),
    ],
)
def test_iterable_encoder(data: Any, expected: Any):
    """IterableEncoder should return a list."""
    assert json.dumps(data, cls=utils.IterableEncoder) == expected
