"""Artifact storage functions."""
from pathlib import Path

from django.core.files.storage import Storage, get_storage_class


def get_artifact_storage() -> Storage:
    """Return the instantiated Archive storage class."""
    from django.conf import settings

    ArchiveStorageClass = get_storage_class(settings.ARCHIVE_STORAGE)

    if settings.ARCHIVE_STORAGE == "django.core.files.storage.FileSystemStorage":
        Path(settings.ARCHIVE_STORAGE_OPTIONS["location"]).mkdir(parents=True, exist_ok=True)

    return ArchiveStorageClass(**settings.ARCHIVE_STORAGE_OPTIONS)
