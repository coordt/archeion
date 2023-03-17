"""Application entry point."""
from django.apps import AppConfig


class IndexConfig(AppConfig):
    """Index application config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "archeion.index"
