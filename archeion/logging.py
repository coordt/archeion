"""Logging and user notification."""
from typing import List, Optional, Union

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from django.utils import timezone
from rich.console import Console
from rich.padding import Padding
from rich.table import Table

CONSOLE = Console()
ERR_CONSOLE = Console(stderr=True)


def message(
    text: Union[str, List[str]], left_indent: int = 0, color: Optional[str] = None, emoji_name: Optional[str] = None
):
    """Output a message to the console."""
    if not isinstance(text, list):
        text = [text]
    icon = f":{emoji_name.strip(':')}: " if emoji_name else ""
    color = f"[{color}]" if color else ""
    end_color = "[/]" if color else ""
    msg = f"{color}{icon}{text[0]}{end_color}"

    CONSOLE.print(Padding(msg, (0, 0, 0, left_indent)))

    extra_indent = 2 if icon else 0

    for line in text[1:]:
        CONSOLE.print(Padding(f"{color}{line}{end_color}", (1, 0, 0, left_indent + extra_indent)))


def warning(text: Union[str, List[str]], left_indent: int = 0) -> None:
    """Output a warning message with optional indentation."""
    message(text, left_indent=left_indent, color="#ffa62b", emoji_name="hand")


def error(text: Union[str, List[str]], left_indent: int = 0) -> None:
    """Output an error message with optional indentation."""
    message(text, left_indent=left_indent, color="#ba3c5b", emoji_name="exclamation_mark")


def info(text: Union[str, List[str]], left_indent: int = 0) -> None:
    """Output an info message with optional indentation."""
    message(text, left_indent=left_indent, color="#004578", emoji_name="information")


def success(text: str, left_indent: int = 0) -> None:
    """Output a success message with optional indentation."""
    message(text, left_indent=left_indent, color="#4EBF71", emoji_name="white_check_mark")


def hint(text: Union[str, List[str]], left_indent: int = 0) -> None:
    """Output a hint message with optional indentation."""
    if not isinstance(text, list):
        text = [text]
    text.insert(0, "Hint:")
    message(text, left_indent=left_indent, color="#ffa62b", emoji_name="light_bulb")


def rule(style: Optional[str] = None, title: Optional[str] = None) -> None:
    """Output a horizontal rule with optional title and style."""
    CONSOLE.rule(style=style or "", title=title or "")


@dataclass
class RuntimeStats:
    """Mutable stats counter for logging archiving timing info to CLI output."""

    skipped: int = 0
    succeeded: int = 0
    failed: int = 0

    parse_start_ts: Optional[datetime] = None
    parse_end_ts: Optional[datetime] = None

    index_start_ts: Optional[datetime] = None
    index_end_ts: Optional[datetime] = None

    archiving_start_ts: Optional[datetime] = None
    archiving_end_ts: Optional[datetime] = None


_LAST_RUN_STATS = RuntimeStats()


def log_cli_command(subcommand: str, subcommand_args: List[str], pwd: str):
    """Log a command to the CLI."""
    from archeion import __version__

    cmd = " ".join(("archeion", subcommand, *subcommand_args))

    ERR_CONSOLE.print(f"[black i] [{timezone.localtime():%Y-%m-%d %H:%M:%S}] ArchiveBox v{__version__}: {cmd}[/]")
    ERR_CONSOLE.print(f"[black]    > {pwd}[/]")
    ERR_CONSOLE.print()


def pretty_path(path: Union[Path, str]) -> str:
    """Convert paths like ``.../ArchiveBox/archivebox/../output/abc into output/abc``."""
    pwd = Path(".").resolve()
    return str(Path(path).relative_to(pwd))


def printable_folders(folders: dict) -> str:
    """Convert a dictionary of folder->Link to a newline-delimited string."""
    return "\n".join(f'{folder} {link and link.url} "{link and link.title}"' for folder, link in folders.items())


def config_report(config: dict, prefix: str = "") -> str:
    """Convert a config dictionary to a report string."""
    return f"\n{prefix}".join(
        f"{key}={val}" for key, val in config.items() if not (isinstance(val, dict) or callable(val))
    )


def dependency_report() -> Table:
    """
    Create an output table of the dependencies.

    Returns:
        A Rich Table suitable for outputting to the console
    """
    from archeion.dependency import get_dependency_info

    table = Table("Name", "Enabled", "Valid", "Version", "Path", title="Dependency Versions")
    dependencies = get_dependency_info()
    for name, info in dependencies.items():
        if info.enabled:
            table.add_row(
                name,
                ":white_check_mark: [green]Enabled[/]",
                ":white_check_mark: [green]Valid[/]" if info.valid else ":cross_mark: [red]Invalid[/]",
                info.version,
                info.path,
            )
        else:
            table.add_row(
                name,
                ":heavy_minus_sign: [bright_black]Disabled[/]",
                "[bright_black]n/a[/]",
                "[bright_black]n/a[/]",
                "[bright_black]n/a[/]",
            )
    return table


def format_size_in_bytes(size: int) -> str:
    """
    Format a size in bytes into a human-readable format.

    Args:
        size: The size in bytes

    Returns:
        The size in a human-readable format
    """
    power = 2**10
    n = 0
    power_labels = {0: "bytes", 1: "KB", 2: "MB", 3: "GB", 4: "TB"}
    new_size = float(size)
    while new_size >= power:
        new_size /= power
        n += 1
    return f"{new_size:.2f} {power_labels[n]}"
