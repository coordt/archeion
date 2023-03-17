"""Entrypoint for the users app."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    """Entrypoint for the users app."""

    name = "archeion.users"
    verbose_name = _("Users")
