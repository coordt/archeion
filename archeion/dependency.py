"""External binary dependency management."""

import importlib.resources
import shutil
import subprocess  # nosec B404
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Sequence, Union

from django.conf import settings

from archeion.logging import error, hint, info, success


def bin_path(binary: Optional[str] = None, cwd: Optional[Union[str, Path]] = None) -> Optional[str]:
    """The path to the binary."""
    if binary is None:
        return None

    cwd = cwd or settings.APPS_DIR

    node_modules_bin = Path(cwd) / "node_modules" / ".bin" / binary

    if node_modules_bin.exists():
        return str(node_modules_bin.resolve())

    return shutil.which(str(Path(binary).expanduser().resolve())) or shutil.which(str(binary)) or binary


def run_shell(
    command: Union[str, Sequence[str]], cwd: Optional[Union[str, Path]] = None, **kwargs
) -> subprocess.CompletedProcess:
    """Run a command in the shell and return the result."""
    keyword_args = {
        "cwd": cwd,
        "check": False,
        "capture_output": True,
        "text": True,
        "shell": True,
    }
    keyword_args.update({key: str(val) for key, val in kwargs.items()})
    return subprocess.run(args=command, **keyword_args)  # type: ignore[call-overload]


@dataclass
class DependencyConfig:
    """The dependency configuration."""

    path: str
    version: str
    enabled: bool
    valid: bool


def get_dependency_info() -> Dict[str, DependencyConfig]:
    """
    Get the dependency information based on the archiver configuration.

    Returns:
        A dictionary with the name
    """
    return {}
    # archivers = get_all_archivers()
    # return {
    #     archiver["name"]: DependencyConfig(
    #         path=archiver["class"].tool_binary,
    #         version=archiver["class"].tool_version,
    #         enabled=archiver["enabled"],
    #         valid=archiver["class"].is_valid,
    #     )
    #     if archiver["enabled"]
    #     else DependencyConfig(
    #         path="n/a",
    #         version="n/a",
    #         enabled=archiver["enabled"],
    #         valid=False,
    #     )
    #     for archiver in archivers
    # }


def get_python_info() -> DependencyConfig:
    """
    Get the python dependency info.

    Returns:
        Information about the python dependency.
    """
    import sys

    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    return DependencyConfig(path=sys.executable, version=version, enabled=True, valid=True)


def get_youtubedl_info() -> DependencyConfig:
    """
    Get the youtube-dl dependency info.

    Returns:
        Information about the youtube-dl dependency.
    """
    path = bin_path("youtube-dl")
    output = run_shell(f"{path} --version")
    if output.returncode != 0:
        return DependencyConfig(
            path=path,
            version="n/a",
            enabled=False,
            valid=False,
        )
    return DependencyConfig(
        path=path,
        version=output.stdout.strip(),
        enabled=True,
        valid=True,
    )


def install_youtube_dl(archive_root: Path) -> None:
    """
    Install the youtube-dl dependency, if missing.
    """
    info("Checking YouTube-DL availability...", left_indent=2)
    ytdl_info = get_youtubedl_info()

    if ytdl_info.valid:
        success(f"YouTube-DL {ytdl_info.version} is available at {ytdl_info.path}.", left_indent=2)
        return

    info("Installing YouTube-DL...", left_indent=2)
    python_info = get_python_info()
    result = run_shell(
        [
            python_info.path,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "--no-cache-dir",
            "--no-warn-script-location",
            "youtube-dl",
        ],
        cwd=archive_root,
    )
    if result.returncode != 0:
        error(["Failed to install YouTube-DL:", result.stderr])
    new_ytdl_info = get_youtubedl_info()
    if not new_ytdl_info.valid:
        error("Failed to install YouTube-DL. It is not available on the PATH.")
    success(f"YouTube-DL {new_ytdl_info.version} is available at {new_ytdl_info.path}.", left_indent=2)


def get_webdriver_info() -> DependencyConfig:
    """Get the webdriver dependency info."""
    from archeion.archivers.webdriver import WebDriverArchiver

    webdriver = WebDriverArchiver({})

    return DependencyConfig(
        path=webdriver.tool_binary or "n/a",
        version=webdriver.tool_version,
        enabled=webdriver.is_valid,
        valid=webdriver.is_valid,
    )


def check_webdriver() -> None:
    """Check that the webdriver is available."""
    info("Checking WebDriver availability...", left_indent=2)
    webdriver_info = get_webdriver_info()
    if not webdriver_info.valid:
        error("WebDriver is not available.", left_indent=2)
    success(f"WebDriver {webdriver_info.version} is available at {webdriver_info.path}.", left_indent=2)


def get_node_info() -> DependencyConfig:
    """Return dependency configuration for node installed on the system."""
    npm_path = bin_path("npm")
    if npm_path is None:
        return DependencyConfig(
            path="n/a",
            version="n/a",
            enabled=False,
            valid=False,
        )
    node_result = run_shell("node -v")
    npm_result = run_shell(f"{npm_path} -v")
    if node_result.returncode != 0 or npm_result.returncode != 0:
        error("Failed to get node or npm version.", left_indent=2)
        version = "n/a"
    else:
        version = f"{node_result.stdout.strip()} / {npm_result.stdout.strip()}"

    return DependencyConfig(
        path=npm_path,
        version=version,
        enabled=True,
        valid=True,
    )


def install_node(archive_root: Path) -> None:
    """
    Install the node dependency, if missing.
    """
    info("Checking Node availability...", left_indent=2)
    node_info = get_node_info()
    if not node_info.valid:
        error(
            [
                "Several tools require npm for installation",
                "You must first install node using your system package manager",
            ]
        )
        hint(
            [
                "https://docs.npmjs.com/downloading-and-installing-node-js-and-npm",
            ]
        )
        return

    success(f"Node/NPM {node_info.version} is available at {node_info.path}.", left_indent=2)
    cleanup_old_node(archive_root)

    pkg_dir = importlib.resources.files("archeion")
    node_pkg_contents = pkg_dir.joinpath("package.json").read_text()
    archive_root.joinpath("package.json").write_text(node_pkg_contents)

    result = run_shell(
        [
            "npm",
            "install",
            "--prefix",
            str(archive_root),  # force it to put the node_modules dir in this folder
            "--force",  # overwrite any existing node_modules
            "--no-save",  # don't bother saving updating the package.json or package-lock.json file
            "--no-audit",  # don't bother checking for newer versions with security vuln fixes
            "--no-fund",  # hide "please fund our project" messages
            "--loglevel",
            "error",  # only show errors (hide warn/info/debug) during installation
            # these args are written in blood, change with caution
        ],
        cwd=archive_root,
    )
    archive_root.joinpath("package.json").unlink(missing_ok=True)

    if result.returncode != 0:
        error(
            [
                "Failed to install npm packages:",
                result.stderr,
            ],
            left_indent=2,
        )
        hint(f"Try deleting {archive_root}/node_modules and running it again")


def cleanup_old_node(archive_root: Path) -> None:
    """
    Cleanup any old node installation in the archive root.

    Args:
        archive_root: The path to the archive root.
    """
    info("Cleaning up any previous installation...", left_indent=2)
    pkg_json = archive_root / "package.json"
    if pkg_json.exists():
        info(f"Removing {pkg_json}...", left_indent=4)
        pkg_json.unlink(missing_ok=True)
    pkg_lock = archive_root / "package-lock.json"
    if pkg_lock.exists():
        info(f"Removing {pkg_lock}...", left_indent=4)
        pkg_lock.unlink(missing_ok=True)
    node_mods = archive_root / "node_modules"
    if node_mods.exists():
        info(f"Removing {node_mods}...", left_indent=4)
        shutil.rmtree(node_mods, ignore_errors=True)


def install_dependencies(archive_root: Path) -> None:
    """Automatically install all Archeion's dependencies and extras."""
    info("Installing enabled ArchiveBox dependencies automatically...")

    install_youtube_dl(archive_root)

    check_webdriver()

    install_node(archive_root)
