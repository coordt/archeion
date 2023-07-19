"""Artifact storage functions."""
from pathlib import Path

from django.core.exceptions import SuspiciousFileOperation
from django.core.files.base import ContentFile
from django.core.files.storage import Storage, get_storage_class

from archeion.logging import error, success


def get_artifact_storage() -> Storage:
    """Return the instantiated Archive storage class."""
    from django.conf import settings

    ArchiveStorageClass = get_storage_class(settings.ARCHIVE_STORAGE)  # noqa: N806

    if settings.ARCHIVE_STORAGE == "django.core.files.storage.FileSystemStorage":
        Path(settings.ARCHIVE_STORAGE_OPTIONS["location"]).mkdir(parents=True, exist_ok=True)

    return ArchiveStorageClass(**settings.ARCHIVE_STORAGE_OPTIONS)


def save_artifact_file(filepath: str, content: ContentFile, plugin_name: str) -> bool:
    """Save an artifact file to the archive storage."""
    try:
        storage = get_artifact_storage()
        if storage.exists(filepath):
            storage.delete(filepath)
        storage.save(filepath, content)
        success(f"Saved {plugin_name} to {filepath}")
        return True
    except SuspiciousFileOperation as e:  # pragma: no coverage
        error([f"{plugin_name} failed:", e])
        return False
