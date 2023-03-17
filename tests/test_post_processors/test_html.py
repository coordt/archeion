"""Tests for HTML html_metadata."""
import datetime
import json
from pathlib import Path

import pytest

from archeion.post_processors.html_metadata import Normalizer

from .normalized_data import (
    csstricks_html,
    github_html,
    medium_html,
    missing_data_html,
    uxcollective_html,
)

METADATA_DIR = Path(__file__).parent.parent / "fixtures" / "html-metadata"


@pytest.mark.parametrize(
    ["src_file", "expected"],
    [
        pytest.param(
            METADATA_DIR / "missing-data.json",
            missing_data_html,
            id="missing-data",
        ),
        pytest.param(
            METADATA_DIR / "github.json",
            github_html,
            id="github",
        ),
        pytest.param(
            METADATA_DIR / "medium.json",
            medium_html,
            id="medium",
        ),
        pytest.param(
            METADATA_DIR / "uxcollective.json",
            uxcollective_html,
            id="uxcollective",
        ),
        pytest.param(
            METADATA_DIR / "csstricks.json",
            csstricks_html,
            id="csstricks",
        ),
    ],
)
def test_normalize_html(freezer, src_file: Path, expected: dict):
    """
    Normalizer should properly parse HTML html_metadata.
    """
    freezer.move_to(datetime.datetime.now())  # Fix the time
    expected["dateArchived"] = datetime.datetime.now()

    if expected["datePublished"] is None:
        expected["datePublished"] = datetime.datetime.now(tz=datetime.timezone.utc)

    raw_data = json.loads(src_file.read_text())
    data = {
        "github": {},
        "html": raw_data["html"],
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
