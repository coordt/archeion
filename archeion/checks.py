"""Functions that check and validate the setup."""


def check_db() -> None:
    """Check if the database is compatible with this version of the program."""
    from django.conf import settings
    from django.db import connection
    from django.db.utils import OperationalError
    from rich.padding import Padding

    from archeion.logging import ERR_CONSOLE

    if settings.DATABASES["default"]["ENGINE"] != "django.db.backends.sqlite3":
        return

    # Check to make sure JSON extension is available in our Sqlite3 instance
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT JSON(\'{"a": "b"}\')')
            current_mode = cursor.execute("PRAGMA journal_mode")
            if current_mode != "wal":
                cursor.execute("PRAGMA journal_mode=wal;")

            # Set max blocking delay for concurrent writes and write sync mode
            # https://litestream.io/tips/#busy-timeout
            cursor.execute("PRAGMA busy_timeout = 5000;")
            cursor.execute("PRAGMA synchronous = NORMAL;")
    except OperationalError as e:
        ERR_CONSOLE.print(f"[red]:x: Your SQLite3 version is missing the required JSON1 extension: {e}[\\]")
        ERR_CONSOLE.print(
            Padding(
                "[magenta][bold]Hint:[/bold] Upgrade your Python version or install the extension manually:"
                "https://code.djangoproject.com/wiki/JSON1Extension[/]",
                (0, 0, 0, 2),
            )
        )
