"""Set up an archive."""

import os
from pathlib import Path

from click import Abort, UsageError
from django.core.management import call_command

from archeion import __version__
from archeion.index.storage import get_artifact_storage
from archeion.logging import error, hint, info, rule, success, warning
from archeion.utils import temp_cd


def log_not_empty(force: bool, archive_root: Path) -> None:
    """Inform the user that the destination directory is not empty."""
    if force:
        warning(
            [
                f"The archive root ({archive_root}) appears to already have files in it.",
                "Because --force was passed, Archeion will initialize anyway (which may overwrite existing files).",
            ]
        )
    else:
        error(
            [
                f"The archive root ({archive_root}) appears to already have files in it",
                "You must run init in a completely empty directory, or an existing data folder.",
            ]
        )
        hint("If you want to force Archeion to initialize anyway, use --force.")


def migrate_database() -> None:
    """Migrate the database if necessary."""
    from io import StringIO

    out = StringIO()
    call_command("migrate", "--plan", stdout=out)

    if "No planned migration operations" in out.getvalue():
        success("The database is already up to date.")
    else:
        info(f"Migrating the Archeion {__version__} database index...")
        call_command("migrate")


def init(archive_root: Path, force: bool = False) -> None:
    """
    Initialize a new Archeion archive in the archive_root directory.

    Args:
        archive_root: The root directory of the new archive.
        force: If True, the archive will be initialized even if the directory isn't empty.

    Raises:
        UsageError: If the archive_root directory doesn't exist.
    """
    from archeion.config import ALLOWED_IN_OUTPUT_DIR, CONFIG_FILENAME, SOURCES_DIR_NAME, write_config_file

    archive_root.mkdir(exist_ok=True)
    files_not_allowed = {str(path) for path in archive_root.iterdir()} - ALLOWED_IN_OUTPUT_DIR

    if len(files_not_allowed) > 0:
        info(f"Initializing the Archeion {__version__} archive in `{archive_root}`...")
        rule()
    else:
        log_not_empty(force, archive_root)
        if not force:
            raise UsageError("Exiting...")

    info(f"Setting up the source cache directory ({SOURCES_DIR_NAME})...")
    archive_root.joinpath(SOURCES_DIR_NAME).mkdir(exist_ok=True)

    info(f"Setting up the configuration file ({CONFIG_FILENAME})...")
    write_config_file(archive_root=archive_root)

    info("Initializing Django...")
    setup_django(archive_root=archive_root)

    info("Setting up the artifact storage ...")
    get_artifact_storage()

    migrate_database()

    setup_superuser()


def setup_superuser() -> None:
    """Create a superuser if it doesn't already exist."""
    from archeion.users.models import User

    if not User.objects.filter(is_superuser=True).exists():
        info("Creating admin user account for the web UI...")
        call_command("createsuperuser", interactive=True)


def setup_django(archive_root: Path) -> None:
    """
    Make sure Django's settings are available and load the settings with the new config file.

    Args:
        archive_root: The Path to the archive root
    """
    import sys

    import django

    from archeion.checks import check_db

    package_dir = Path(__file__).resolve().parent

    sys.path.append(str(package_dir))
    base_settings_path = package_dir.joinpath("config/settings/base.py")
    if not base_settings_path.exists():
        Abort(f"The base settings was not found at `{base_settings_path}`")

    config_mode = os.environ.get("ARCHEION_MODE", "local")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.settings.{config_mode}")

    with temp_cd(archive_root):
        django.setup()

    check_db()
