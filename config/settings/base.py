"""
Base settings to build other settings files upon.
"""

from pathlib import Path

from environs import Env, _dj_cache_url_parser, _dj_db_url_parser

from archeion.autocast import autocast_value
from archeion.config import get_settings

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

APPS_DIR = ROOT_DIR / "archeion"
env = Env()
env.read_env(str(ROOT_DIR / ".env"), verbose=True)
config = get_settings()

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = config.server_config.debug
TIME_ZONE = config.server_config.time_zone
LANGUAGE_CODE = "en-us"
SITE_ID = 1
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [str(ROOT_DIR / "locale")]
SECRET_KEY = config.server_config.secret_key
ALLOWED_HOSTS = config.server_config.allowed_hosts

# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    "default": _dj_cache_url_parser(config.cache_url),
}

# URLS
# ------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    # "whitenoise.runserver_nostatic",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.humanize", # Handy template tags
    "django.contrib.admin",
    "django.forms",
]
THIRD_PARTY_APPS = [
    "crispy_forms",
    "crispy_bootstrap5",
    "corsheaders",
    "django_extensions",
    "django_tables2",
    "django_filters",
    "fontawesomefree",
]

LOCAL_APPS = [
    "archeion.users",
    "archeion.index",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# AUTHENTICATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]
AUTH_USER_MODEL = "users.User"
LOGIN_URL = "login"
APPEND_SLASH = True

# PASSWORDS
# ------------------------------------------------------------------------------
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
STATIC_ROOT = str(ROOT_DIR / "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(APPS_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
WHITENOISE_USE_FINDERS = True

# MEDIA
# ------------------------------------------------------------------------------
MEDIA_ROOT = str(config.archive_root / config.artifacts_dir_name)
MEDIA_URL = "/archives/"
FILE_UPLOAD_PERMISSIONS = config.artifact_storage_options.get("file_permissions_mode", 0o644)
FILE_UPLOAD_DIRECTORY_PERMISSIONS = config.artifact_storage_options.get("directory_permissions_mode", 0o755)

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(ROOT_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "SAMEORIGIN"

# EMAIL
# ------------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_TIMEOUT = 5

DEFAULT_FROM_EMAIL = env("ARCHEION_DEFAULT_FROM_EMAIL", default="Archeion <noreply@archeion.dev>")
SERVER_EMAIL = env("ARCHEION_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
EMAIL_SUBJECT_PREFIX = env("ARCHEION_EMAIL_SUBJECT_PREFIX", default="[Archeion]")

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = env.str("ARCHEION_ADMIN_URL", default="admin/")
ADMINS = [("No Reply", "no-reply@example.com")]
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {"verbose": {"format": "%(name)s: %(message)s"}},
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "INFO",
            "class": "rich.logging.RichHandler",
            "formatter": "verbose",
            "show_path": False,
            "rich_tracebacks": True,
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "WDM": {"handlers": ["console"], "level": "ERROR", "propagate": True},
        "seleniumwire": {"handlers": ["console"], "level": "ERROR", "propagate": True},
        "django.request": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
        # "django.security.DisallowedHost": {
        #     "level": "ERROR",
        #     "handlers": ["console", "mail_admins"],
        #     "propagate": True,
        # },
    },
}

# django-cors-headers - https://github.com/adamchainz/django-cors-headers#setup
CORS_URLS_REGEX = r"^/api/.*$"

# DATABASES
# ------------------------------------------------------------------------------

# DB setup is sometimes modified at runtime by setup_django() in config.py

DATABASE_CONFIG = _dj_db_url_parser(config.database_url)
DATABASE_CONFIG["TIME_ZONE"] = TIME_ZONE

if "OPTIONS" not in DATABASE_CONFIG:
    DATABASE_CONFIG["OPTIONS"] = {}

DATABASE_CONFIG["OPTIONS"] = {key: autocast_value(value) for key, value in DATABASE_CONFIG["OPTIONS"].items()}

DATABASES = {
    "default": DATABASE_CONFIG,
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Archeion Stuff
# ------------------------------------------------------------------------------

ARCHIVE_STORAGE = config.artifact_storage
ARCHIVE_STORAGE_OPTIONS = config.artifact_storage_options

DANDELION_TOKEN = config.dandelion_token

COMMAND_TIMEOUT = config.timeout
MEDIA_TIMEOUT = config.media_timeout
URL_BLACKLIST = config.url_blacklist
URL_WHITELIST = config.url_whitelist
CHECK_SSL_VALIDITY = config.check_ssl_validity

CONFIG_FILENAME = config.config_filename
ARTIFACTS_DIR_NAME = "artifacts"
SOURCES_DIR_NAME = "sources"
PUBLIC_INDEX = config.server_config.public_index
PUBLIC_SNAPSHOTS = config.server_config.public_snapshots
PUBLIC_ADD_VIEW = config.server_config.public_add_view
ITEMS_PER_PAGE = config.server_config.snapshots_per_page
PREVIEW_ORIGINALS = config.server_config.preview_originals

SEARCH_CONFIG = config.search_config


LINK_PARSERS = [
    "archeion.parsers.generic_html.parse_html_links",
    "archeion.parsers.generic_feed.parse_generic_feed",
    "archeion.parsers.generic_text.parse_text",
]

ARCHIVERS = config.archivers
POST_PROCESSORS = config.post_processors

# Based on https://github.com/mpchadwick/tracking-query-params-registry with additions
STRIPPABLE_QUERY_PARAMS = {
    "_branch_match_id",
    "_bta_c",
    "_bta_tid",
    "_ga",
    "_ke",
    "campid",
    "customid",
    "dm_i",
    "ef_id",
    "epik",
    "fbclid",
    "gclid",
    "gclsrc",
    "gdffi",
    "gdfms",
    "gdftrk",
    "hsa_acc",
    "hsa_ad",
    "hsa_cam",
    "hsa_grp",
    "hsa_kw",
    "hsa_mt",
    "hsa_net",
    "hsa_src",
    "hsa_tgt",
    "hsa_ver",
    "igshid",
    "matomo_campaign",
    "matomo_cid",
    "matomo_content",
    "matomo_group",
    "matomo_keyword",
    "matomo_medium",
    "matomo_placement",
    "matomo_source",
    "mc_cid",
    "mc_eid",
    "mkcid",
    "mkevt",
    "mkrid",
    "mkwid",
    "msclkid",
    "mtm_campaign",
    "mtm_cid",
    "mtm_content",
    "mtm_group",
    "mtm_keyword",
    "mtm_medium",
    "mtm_placement",
    "mtm_source",
    "name",
    "pcrid",
    "piwik_campaign",
    "piwik_keyword",
    "piwik_kwd",
    "pk_campaign",
    "pk_keyword",
    "pk_kwd",
    "promotion_id",
    "redirect_log_mongo_id",
    "redirect_mongo_id",
    "ref",
    "s_kwcid",
    "sb_referer_host",
    "si",
    "toolid",
    "trk_contact",
    "trk_module",
    "trk_msg",
    "trk_sid",
    "utm_campaign",
    "utm_content",
    "utm_id",
    "utm_medium",
    "utm_source",
    "utm_term",
}

OG_TYPE_MAP = {
    "music.song": "https://schema.org/MusicRecording",
    "music.album": "https://schema.org/MusicAlbum",
    "music.playlist": "https://schema.org/MusicPlaylist",
    "music.radio_station": "https://schema.org/Organization",
    "video.movie": "https://schema.org/Movie",
    "video.episode": "https://schema.org/Episode",
    "video.tv_show": "https://schema.org/TVSeries",
    "video.other": "https://schema.org/VideoObject",
    "article": "https://schema.org/Article",
    "book": "https://schema.org/Book",
    "profile": "https://schema.org/Person",
    "object": "https://schema.org/Thing",
}

OG_TAG_MAP = {
    "og:url": "source",
    "og:title": "headline",
    "og:description": "description",
    "og:site_name": "publisher",
    "og:published_time": "datePublished",
    "og:tag": "keywords",
    "og:type": "type",
    "article:author": "author",
    "article:published_time": "datePublished",
    "og:video:tag": "keywords",
    "og:article:tag": "keywords",
    "og:book:tag": "keywords",
    "og:music:tag": "keywords",
}
