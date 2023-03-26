"""Tests for microdata html_metadata."""
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
            METADATA_DIR / "missing-data.json",
            {
                "type": "https://schema.org/CreativeWork",
                "headline": None,
                "description": None,
                "author": None,
                "publisher": None,
                "keywords": set(),
                "datePublished": None,
                "source": None,
                "encodingFormat": "text/html",
                "sourceEncodingFormat": "text/html",
            },
            id="missing-data",
        ),
        pytest.param(
            METADATA_DIR / "github.json",
            {
                "type": "http://schema.org/SoftwareSourceCode",
                "headline": "archivy",
                "description": None,
                "author": [{"type": "https://schema.org/Person", "name": "archivy"}],
                "publisher": None,
                "keywords": set(),
                "datePublished": None,
                "source": None,
                "encodingFormat": "text/html",
                "sourceEncodingFormat": "text/html",
            },
            id="github",
        ),
        pytest.param(
            METADATA_DIR / "medium.json",
            {
                "type": "https://schema.org/CreativeWork",
                "headline": None,
                "description": None,
                "author": None,
                "publisher": None,
                "keywords": set(),
                "datePublished": None,
                "source": None,
                "encodingFormat": "text/html",
                "sourceEncodingFormat": "text/html",
            },
            id="medium",
        ),
        pytest.param(
            METADATA_DIR / "uxcollective.json",
            {
                "type": "https://schema.org/CreativeWork",
                "headline": None,
                "description": None,
                "author": None,
                "publisher": None,
                "keywords": set(),
                "datePublished": None,
                "source": None,
                "encodingFormat": "text/html",
                "sourceEncodingFormat": "text/html",
            },
            id="uxcollective",
        ),
    ],
)
def test_normalize_microdata(freezer, src_file: Path, expected: dict):
    """
    Normalizer should properly parse microdata html_metadata.
    """
    freezer.move_to(datetime.datetime.now())  # Fix the time
    expected["dateArchived"] = datetime.datetime.now()

    if expected["datePublished"] is None:
        expected["datePublished"] = datetime.datetime.now(tz=datetime.timezone.utc)

    raw_data = json.loads(src_file.read_text())
    data = {
        "github": {},
        "html": [],
        "microdata": raw_data["microdata"],
        "json-ld": [],
        "opengraph": [],
        "microformat": [],
        "rdfa": [],
        "dublincore": [],
    }
    norm = Normalizer(data).normalized_metadata()
    norm["dateArchived"] = datetime.datetime.now()
    assert norm == expected
