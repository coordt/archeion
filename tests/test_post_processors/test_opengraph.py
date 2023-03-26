"""Tests for Open Graph html_metadata."""
import datetime
import json
from pathlib import Path

import dateutil.parser
import pytest
from django.conf import settings

from archeion.post_processors.html_metadata import Normalizer

METADATA_DIR = Path(__file__).parent.parent / "fixtures" / "html-metadata"


@pytest.mark.parametrize(
    ["src_file", "expected"],
    [
        pytest.param(
            METADATA_DIR / "github.json",
            {
                "type": settings.OG_TYPE_MAP["object"],
                "headline": "archivy/archivy",
                "description": (
                    "Archivy is a self-hosted knowledge repository that allows you to safely preserve useful content "
                    "that contributes to your own personal, searchable and extendable wiki. - archivy/archivy"
                ),
                "author": None,
                "publisher": [{"type": "https://schema.org/Organization", "name": "GitHub"}],
                "keywords": set(),
                "datePublished": None,
                "source": "https://github.com/archivy/archivy",
                "encodingFormat": "text/html",
                "sourceEncodingFormat": "text/html",
            },
            id="github",
        ),
        pytest.param(
            METADATA_DIR / "medium.json",
            {
                "type": settings.OG_TYPE_MAP["article"],
                "headline": "Fetching Better Beer Recommendations with Collie (Part 1)",
                "description": "Getting data, training a model, and talking about beer!",
                "author": [
                    {
                        "type": "https://schema.org/Person",
                        "name": "https://medium.com/@nathancooperjones",
                    }
                ],
                "publisher": [{"type": "https://schema.org/Organization", "name": "Medium"}],
                "keywords": set(),
                "datePublished": dateutil.parser.isoparse("2021-05-04T20:16:56.056Z"),
                "source": (
                    "https://medium.com/shoprunner/fetching-better-beer-recommendations-"
                    "with-collie-part-1-18c73ab30fbd"
                ),
                "encodingFormat": "text/html",
                "sourceEncodingFormat": "text/html",
            },
            id="medium",
        ),
        pytest.param(
            METADATA_DIR / "uxcollective.json",
            {
                "type": settings.OG_TYPE_MAP["article"],
                "headline": "How to design data visualizations that are actually valuable",
                "description": (
                    "A guide to understanding how people interpret data and choosing elements to create "
                    "clear visualizations"
                ),
                "author": [
                    {
                        "type": "https://schema.org/Person",
                        "name": "https://angelica08.medium.com",
                    }
                ],
                "publisher": [{"type": "https://schema.org/Organization", "name": "Medium"}],
                "keywords": set(),
                "datePublished": dateutil.parser.isoparse("2021-07-21T17:53:30.905Z"),
                "source": "https://uxdesign.cc/how-to-design-data-visualizations-that-are-actually-valuable-e8b752835b9a",  # noqa: E501
                "encodingFormat": "text/html",
                "sourceEncodingFormat": "text/html",
            },
            id="uxcollective",
        ),
    ],
)
def test_normalize_opengraph(freezer, src_file: Path, expected: dict):
    """
    Normalizer should properly parse opengraph data.
    """
    freezer.move_to(datetime.datetime.now())  # Fix the time
    expected["dateArchived"] = datetime.datetime.now()

    if expected["datePublished"] is None:
        expected["datePublished"] = datetime.datetime.now(tz=datetime.timezone.utc)

    raw_data = json.loads(src_file.read_text())
    data = {
        "github": {},
        "microdata": [],
        "json-ld": [],
        "opengraph": raw_data["opengraph"],
        "microformat": [],
        "rdfa": [],
        "dublincore": [],
    }
    norm = Normalizer(data).normalized_metadata()
    norm["dateArchived"] = datetime.datetime.now()
    assert norm == expected
