"""Tests of catalog.extract_html."""

import json
from json import JSONEncoder
from pathlib import Path

import pytest

from archeion.post_processors.html_metadata import extract_metadata

# from tests.extract_test_metadata import CustomEncoder

FIXTURE_DIR = Path(__file__).parent.parent / "fixtures"
HTML_METADATA = FIXTURE_DIR / "html-metadata"


class CustomEncoder(JSONEncoder):
    """
    A custom encoder that sorts list items.
    """

    def default(self, obj):
        """Check for iterables and sort them."""
        try:
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable).sort()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


@pytest.mark.parametrize(
    ["page_source", "expected"],
    [
        pytest.param(
            HTML_METADATA / "all.html",
            HTML_METADATA / "all.json",
            id="all",
        ),
        pytest.param(
            HTML_METADATA / "multiple-og.html",
            HTML_METADATA / "multiple-og.json",
            id="multiple-og",
        ),
        pytest.param(
            HTML_METADATA / "csstricks.html",
            HTML_METADATA / "csstricks.json",
            id="cssstricks",
        ),
        pytest.param(
            HTML_METADATA / "github.html",
            HTML_METADATA / "github.json",
            id="github",
        ),
        pytest.param(
            HTML_METADATA / "medium.html",
            HTML_METADATA / "medium.json",
            id="medium",
        ),
        pytest.param(
            HTML_METADATA / "uxcollective.html",
            HTML_METADATA / "uxcollective.json",
            id="uxcollective",
        ),
        pytest.param(
            HTML_METADATA / "yoast.html",
            HTML_METADATA / "yoast.json",
            id="yoast",
        ),
    ],
)
def test_extract_metadata(page_source: Path, expected: Path):
    """Source documents with different combinations of html_metadata should provide expected results."""
    import pprint

    page = page_source.read_text()
    expected_data = json.loads(expected.read_text())
    output = extract_metadata(
        page,
    )

    # This step is necessary to deal with the keyword set() and get rid of rdfa
    del expected_data["rdfa"]  # RDFa includes anonymous nodes with random IDs
    del output["rdfa"]
    output = json.loads(json.dumps(output, indent=2, sort_keys=True, cls=CustomEncoder))

    if output != expected_data:
        pprint.pprint(output)
    assert output == expected_data
