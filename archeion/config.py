"""Configuration setup for Archeion."""
from copy import deepcopy
from pathlib import Path, PosixPath, WindowsPath
from typing import Any, Dict, List, Optional, Pattern

import yaml
from pydantic import BaseSettings, Field

from archeion.index import setup

SETTINGS = None

CONFIG_FILENAME = "config.yaml"
ARTIFACTS_DIR_NAME = "artifacts"
SOURCES_DIR_NAME = "sources"
ALLOWED_IN_OUTPUT_DIR = {
    ".gitignore",
    "lost+found",
    ".DS_Store",
    ".venv",
    "venv",
    "virtualenv",
    ".virtualenv",
    "node_modules",
    ARTIFACTS_DIR_NAME,
    CONFIG_FILENAME,
    SOURCES_DIR_NAME,
    "*.sqlite3",
    "*.sqlite3-wal",
    "*.sqlite3-shm",
}

DEFAULT_SETTINGS: Dict[str, Any] = {
    "artifact_storage": "django.core.files.storage.FileSystemStorage",
    "artifact_storage_options": {
        "location": "",  # This needs to be fully-qualified, so it is set in ``get_default_settings``
        "base_url": "/archives/",
        "file_permissions_mode": 0o644,
        "directory_permissions_mode": 0o755,
    },
    "timeout": 60,
    "media_timeout": 120,
    "url_blacklist": None,
    "url_whitelist": None,
    "check_ssl_validity": True,
    "cache_url": "locmem://",
    "dandelion_token": None,
    "archivers": [
        {
            "enabled": True,
            "path": "dom.html",
            "class_path": "archeion.archivers.dom.DOMArchiver",
        },
        {
            "enabled": True,
            "path": "headers.json",
            "class_path": "archeion.archivers.headers.HeadersArchiver",
        },
        {
            "enabled": True,
            "path": "screenshot.png",
            "class_path": "archeion.archivers.screenshot.ScreenshotArchiver",
            "resolution": (1440, 2000),
        },
        {
            "enabled": True,
            "path": "print.pdf",
            "class_path": "archeion.archivers.pdf.PDFArchiver",
        },
        {
            "enabled": False,
            "class_path": "archeion.archivers.wget.WgetArchiver",
            # 'user_agent': "",  # TODO: Make this dynamic based on the user's system
            "directories_path": "wget/",
            "save_warc": True,
            "args": [
                "--no-verbose",
                "--adjust-extension",
                "--convert-links",
                "--force-directories",
                "--span-hosts",
                "--no-parent",
            ],
        },
        {
            "enabled": True,
            "path": "singlefile.html",
            "class_path": "archeion.archivers.singlefile.SinglefileArchiver",
            "args": [
                "--dump-content",
            ],
            "browser_args": [
                "--headless",
                "--disable-web-security",
                "--ignore-certificate-errors",
            ],
        },
        {
            "enabled": False,
            "path": "git/",
            "class_path": "archeion.archivers.git.GitArchiver",
            "domains": ["github.com", "bitbucket.org", "gitlab.com", "gist.github.com"],
            "args": [],
        },
        {
            "enabled": False,
            "path": "media/",
            "class_path": "archeion.archivers.youtubedl.YouTubeDLArchiver",
            "max_filesize": "750m",
            "args": [
                "--write-description",
                "--write-info-json",
                "--write-annotations",
                "--write-thumbnail",
                "--no-call-home",
                "--write-sub",
                "--all-subs",
                "--write-auto-sub",
                "--convert-subs=srt",
                "--yes-playlist",
                "--continue",
                "--ignore-errors",
                "--no-abort-on-error",
                "--geo-bypass",
                "--add-metadata",
            ],
        },
    ],
    "post_processors": [],
}


def yaml_config_source(settings: BaseSettings) -> Dict[str, Any]:
    """
    A simple settings source that loads variables from a YAML file.
    """
    import yaml

    encoding = settings.__config__.env_file_encoding
    config_path = Path(CONFIG_FILENAME)
    if config_path.exists():
        return yaml.safe_load(config_path.read_text(encoding))
    return {}


class ArchiverSettings(BaseSettings):
    """Individual settings for an Archiver."""

    enabled: bool
    path: str
    class_path: str
    klass: Optional[Any] = None
    name: Optional[str] = None

    class Config:
        """Archiver settings config."""

        extra = "allow"


class ServerSettings(BaseSettings):
    """Configurations for running Django's server."""

    secret_key: str
    bind_addr: str = "127.0.0.1:8000"
    allowed_hosts: List[str] = ["127.0.0.1", "localhost"]
    debug: bool = False
    public_index: bool = True
    public_snapshots: bool = True
    public_add_view: bool = False
    snapshots_per_page: int = 40
    custom_templates_dir: str = None
    time_zone: str = "UTC"
    preview_originals: bool = True

    class Config:
        """Pydantic config."""

        extra = "allow"


class SearchSettings(BaseSettings):
    """Configurations for searching archives."""

    backend: str = "archeion.search.backends.ripgrep"

    class Config:
        """Pydantic config."""

        extra = "allow"


class Settings(BaseSettings):
    """Configurations for Archeion."""

    server_config: ServerSettings = Field(default_factory=ServerSettings)  # type: ignore[arg-type]
    search_config: SearchSettings = Field(default_factory=SearchSettings)
    archive_root: Path
    artifact_storage: str
    artifact_storage_options: Dict[str, Any]
    timeout: int = Field(default=60, ge=15)
    media_timeout: int = Field(default=120, ge=15)
    dandelion_token: Optional[str] = None
    url_blacklist: Optional[Pattern]
    url_whitelist: Optional[Pattern]
    check_ssl_validity: bool
    archivers: List[ArchiverSettings]
    post_processors: List[ArchiverSettings]
    cache_url: str
    database_url: str
    config_filename: str = CONFIG_FILENAME
    artifacts_dir_name: str = ARTIFACTS_DIR_NAME

    class Config:
        """Pydantic config."""

        env_prefix = "archeion_"
        env_file_encoding = "utf-8"
        extra = "allow"

        @classmethod
        def customise_sources(
            cls,
            init_settings: Any,
            env_settings: Any,
            file_secret_settings: Any,
        ) -> tuple:
            """Change the order of importance of config sources so that config files have top priority."""
            return (
                env_settings,
                file_secret_settings,
                yaml_config_source,
                init_settings,
            )


def get_settings() -> Settings:
    """Return the settings singleton, instantiating them if necessary."""
    global SETTINGS  # noqa: PLW0603

    if SETTINGS is None:
        SETTINGS = get_default_settings()
    return SETTINGS


def get_default_settings(archive_root: Optional[Path] = None) -> Settings:
    """
    Generate the default settings, optionally using the passed archive_root.

    Args:
        archive_root: The path to the archive's root directory. If not provided, the
            root directory of the app is used.

    Returns:
        The default settings.
    """
    import os

    from django.core.management.utils import get_random_secret_key

    from archeion.utils import temp_cd

    if not archive_root:
        archive_root = Path(os.environ.get("ARCHEION_ARCHIVE_ROOT")) or Path.cwd()

    defaults = deepcopy(DEFAULT_SETTINGS)
    defaults["archive_root"] = archive_root
    defaults["secret_key"] = get_random_secret_key()
    defaults["artifact_storage_options"]["location"] = archive_root / ARTIFACTS_DIR_NAME
    defaults["database_url"] = f"sqlite:///{archive_root}/index.sqlite3?timeout=60&check_same_thread=false"

    if not archive_root.exists():
        setup.init(archive_root)

    with temp_cd(archive_root):
        # This allows Pydantic to recognize any .env or config.yaml files in the
        # archive root.
        return Settings(**defaults)


def path_representer(dumper: yaml.SafeDumper, data: Any) -> yaml.ScalarNode:
    """Representer for Path objects."""
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(data))


yaml.add_representer(PosixPath, path_representer, Dumper=yaml.SafeDumper)
yaml.add_representer(WindowsPath, path_representer, Dumper=yaml.SafeDumper)


def write_config_file(archive_root: Path, default_overrides: Optional[Dict[str, Any]] = None) -> None:
    """Write the config file to disk."""
    settings = get_default_settings(archive_root).dict()

    config_path = Path(archive_root) / CONFIG_FILENAME
    if config_path.exists():
        existing_config = yaml.safe_load(config_path.read_text())
        settings.update(existing_config)

    settings.update(default_overrides or {})

    config_path.write_text(yaml.safe_dump(settings, default_flow_style=False))
