"""Tests for Twitter html_metadata."""
import datetime
import json
from pathlib import Path

import pytest

from archeion.post_processors.html_metadata import Normalizer

METADATA_DIR = Path(__file__).parent.parent / "fixtures" / "html-metadata"


@pytest.mark.parametrize(
    ["src_file", "expected"],
    [
        pytest.param(
            METADATA_DIR / "github.json",
            dict(
                type="https://schema.org/CreativeWork",
                headline="archivy/archivy",
                description=(
                    "Archivy is a self-hosted knowledge repository that allows you to safely preserve useful content "
                    "that contributes to your own personal, searchable and extendable wiki. - archivy/archivy"
                ),
                author=None,
                publisher=[
                    {
                        "type": "https://schema.org/Organization",
                        "url": "https://twitter.com/github",
                    }
                ],
                keywords=set(),
                datePublished=None,
                source=None,
                encodingFormat="text/html",
                sourceEncodingFormat="text/html",
            ),
            id="github",
        ),
        pytest.param(
            METADATA_DIR / "medium.json",
            dict(
                type="https://schema.org/CreativeWork",
                headline="Fetching Better Beer Recommendations with Collie (Part 1)",
                description="Getting data, training a model, and talking about beer!",
                author=None,
                publisher=[
                    {
                        "type": "https://schema.org/Organization",
                        "url": "https://twitter.com/shoprunner",
                    }
                ],
                keywords=set(),
                datePublished=None,
                source=None,
                encodingFormat="text/html",
                sourceEncodingFormat="text/html",
            ),
            id="medium",
        ),
        pytest.param(
            METADATA_DIR / "uxcollective.json",
            dict(
                type="https://schema.org/CreativeWork",
                headline="How to design data visualizations that are actually valuable",
                description=(
                    "A guide to understanding how people interpret data and choosing elements to create "
                    "clear visualizations"
                ),
                author=None,
                publisher=[
                    {
                        "type": "https://schema.org/Organization",
                        "url": "https://twitter.com/uxdesigncc",
                    }
                ],
                keywords=set(),
                datePublished=None,
                source=None,
                encodingFormat="text/html",
                sourceEncodingFormat="text/html",
            ),
            id="uxcollective",
        ),
    ],
)
def test_normalize_twitter(freezer, src_file: Path, expected: dict):
    """It should always return a valid output."""
    freezer.move_to(datetime.datetime.now())  # Fix the time
    expected["dateArchived"] = datetime.datetime.now()
    if expected["datePublished"] is None:
        expected["datePublished"] = datetime.datetime.now(tz=datetime.timezone.utc)

    raw_data = json.loads(src_file.read_text())
    data = {
        "github": {},
        "twitter": raw_data["twitter"],
        "microdata": [],
        "json-ld": [],
        "opengraph": [],
        "microformat": [],
        "rdfa": [],
        "dublincore": [],
    }
    norm = Normalizer(data).normalized_metadata()
    norm["dateArchived"] = datetime.datetime.now()
    assert norm == expected
