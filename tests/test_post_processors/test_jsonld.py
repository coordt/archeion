"""Tests for JSON-LD html_metadata."""
import datetime
import json
from pathlib import Path

import dateutil.parser
import pytest

from archeion.post_processors.html_metadata import Normalizer

from .normalized_data import github_jsonld, medium_jsonld, missing_data_jsonld, yoast_jsonld

METADATA_DIR = Path(__file__).parent.parent / "fixtures" / "html-metadata"


@pytest.mark.parametrize(
    ["src_file", "expected"],
    [
        pytest.param(
            METADATA_DIR / "yoast.json",
            yoast_jsonld,
            id="yoast",
        ),
        pytest.param(
            METADATA_DIR / "missing-data.json",
            missing_data_jsonld,
            id="missing-data",
        ),
        pytest.param(
            METADATA_DIR / "github.json",
            github_jsonld,
            id="github",
        ),
        pytest.param(
            METADATA_DIR / "medium.json",
            medium_jsonld,
            id="medium",
        ),
        pytest.param(
            METADATA_DIR / "uxcollective.json",
            {
                "type": "https://schema.org/NewsArticle",
                "headline": "How to design data visualizations that are actually valuable",
                "description": (
                    "Great visualizations help people quickly and accurately make sense of the data so they can make "
                    "appropriate decisions. These types of visualizations optimize for the human visual system "
                    "making\u2026"
                ),
                "author": [
                    {
                        "type": "https://schema.org/Person",
                        "name": "Angelica Gutierrez",
                        "url": "https://angelica08.medium.com",
                    }
                ],
                "publisher": [
                    {
                        "type": "https://schema.org/Organization",
                        "name": "UX Collective",
                        "url": "uxdesign.cc",
                        "logo": {
                            "type": "ImageObject",
                            "width": 360,
                            "height": 60,
                            "url": "https://miro.medium.com/max/720/1*9V9oqYyYnfP5yy7cb7YTMQ.png",
                        },
                    }
                ],
                "keywords": set(),
                "datePublished": dateutil.parser.isoparse("2021-07-11T01:15:44.247Z"),
                "source": "https://uxdesign.cc/how-to-design-data-visualizations-that-are-actually-valuable-e8b752835b9a",  # noqa: E501
                "encodingFormat": "text/html",
                "sourceEncodingFormat": "text/html",
            },
            id="uxcollective",
        ),
    ],
)
@pytest.mark.vcr()
def test_normalize_jsonld(freezer, src_file: Path, expected: dict):
    """
    Normalizer should properly parse json-ld data.
    """
    freezer.move_to(datetime.datetime.now())  # Fix the time
    expected["dateArchived"] = datetime.datetime.now()

    if expected.get("datePublished") is None:
        expected["datePublished"] = datetime.datetime.now(tz=datetime.timezone.utc)

    raw_data = json.loads(src_file.read_text())
    data = {
        "github": {},
        "microdata": [],
        "json-ld": raw_data["json-ld"],
        "opengraph": [],
        "microformat": [],
        "rdfa": [],
        "dublincore": [],
    }
    norm = Normalizer(data).normalized_metadata()
    norm["dateArchived"] = datetime.datetime.now()
    assert norm == expected
