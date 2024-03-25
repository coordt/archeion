"""Test configuration."""

from pathlib import Path

import pytest

from archeion.users.models import User
from archeion.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture
def fixture_dir() -> Path:
    """Return the fixture directory."""
    return Path(__file__).parent / "tests" / "fixtures"
