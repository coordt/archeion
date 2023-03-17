"""Archive the link using the singlepage CLI utility."""
from typing import Optional

import json
import os
import shutil
import subprocess  # nosec B404
from functools import cached_property
from pathlib import Path

from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation
from django.core.files.base import ContentFile
from django.utils import timezone

from archeion.dependency import bin_path, run_shell
from archeion.index.models import Artifact, ArtifactStatus
from archeion.index.storage import get_artifact_storage
from archeion.logging import error, info, success


def find_chrome_binary() -> Optional[str]:
    """
    Find any installed chrome binaries in the default locations.

    Precedence: Chromium, Chrome, Beta, Canary, Unstable, Dev

    Returns:
        The Chrome binary
    """
    default_executable_paths = (
        "chromium-browser",
        "chromium",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "chrome",
        "google-chrome",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "google-chrome-stable",
        "google-chrome-beta",
        "google-chrome-canary",
        "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
        "google-chrome-unstable",
        "google-chrome-dev",
    )
    for name in default_executable_paths:
        full_path_exists = shutil.which(name)
        if full_path_exists:
            return name

    return None


def find_chrome_data_dir() -> Optional[Path]:
    """
    Find any installed chrome user data directories in the default locations.

    Precedence: Chromium, Chrome, Beta, Canary, Unstable, Dev

    Need to make sure data dir finding precedence order always matches binary finding order.

    Returns:
        The path to the data dir
    """
    default_profile_paths = (
        "~/.config/chromium",
        "~/Library/Application Support/Chromium",
        "~/AppData/Local/Chromium/User Data",
        "~/.config/chrome",
        "~/.config/google-chrome",
        "~/Library/Application Support/Google/Chrome",
        "~/AppData/Local/Google/Chrome/User Data",
        "~/.config/google-chrome-stable",
        "~/.config/google-chrome-beta",
        "~/Library/Application Support/Google/Chrome Canary",
        "~/AppData/Local/Google/Chrome SxS/User Data",
        "~/.config/google-chrome-unstable",
        "~/.config/google-chrome-dev",
    )

    for path in default_profile_paths:
        full_path = Path(path).expanduser().resolve()
        if full_path.exists():
            return full_path

    return None


class SinglefileArchiver:
    """
    Download the link using the singlepage CLI utility.
    """

    plugin_name = "singlefile"

    def __init__(self, config: dict):
        self.config = config
        self.args = config.get(
            "args",
            [
                "--dump-content",
            ],
        )

        if "--dump-content" not in self.args:  # Need this so it outputs to stdout
            self.args.append("--dump-content")

        self.browser_args = set(config.get("browser_args", []))
        self.chrome_binary = find_chrome_binary()

        has_browser_exec = any(arg.startswith("--browser-executable-path") for arg in self.args)
        has_backend = any(arg.startswith("--back-end") for arg in self.args)

        if not has_browser_exec and not has_backend:
            self.args.append(f"--browser-executable-path={self.chrome_binary}")
            self.browser_args.add(f"--user-data-dir={find_chrome_data_dir()}")
            self.browser_args.add("--headless")

        if settings.CHECK_SSL_VALIDITY:
            self.browser_args.add("--disable-web-security")
            self.browser_args.add("--ignore-certificate-errors")

        if not has_backend:
            self.args.append(f"--browser-args={json.dumps(list(self.browser_args))}")

    @cached_property
    def is_valid(self) -> bool:
        """Return True if the plugin is valid."""
        return bool(shutil.which("single-filez")) and bool(self.chrome_binary)

    @cached_property
    def tool_name(self) -> str:
        """Return the tool name."""
        return "SingleFileZ"

    @cached_property
    def tool_version(self) -> str:
        """Return the tool version."""
        result = run_shell(["single-filez", "--version"])
        return result.stdout.strip()

    @cached_property
    def tool_binary(self) -> Optional[Path]:
        """Return the path to the tool."""
        return Path(bin_path("single-filez"))

    async def __call__(self, artifact: Artifact, overwrite: bool = False) -> Artifact:
        """Archive the link."""
        if artifact.status == ArtifactStatus.SUCCEEDED and not overwrite:
            return artifact

        if not self.is_valid:
            artifact.status = ArtifactStatus.FAILED
            error(f"{self.plugin_name} is not valid.")
            return artifact

        info(f"Saving {self.plugin_name}...", left_indent=2)
        artifact.start_ts = timezone.now()
        artifact.output_path = artifact.output_path or "singlefile.html"
        cmd = [str(self.tool_binary), *self.args, artifact.link.url]

        result = subprocess.run(cmd, check=False, capture_output=True, text=False)  # nosec B602
        artifact.end_ts = timezone.now()
        if result.stderr:
            error([f"{self.plugin_name} failed with stderr:", result.stderr.decode("utf-8")])
            artifact.status = ArtifactStatus.FAILED
            return artifact
        if result.returncode != 0:
            artifact.status = ArtifactStatus.FAILED
            error(result.stderr.decode("utf-8"))
            return artifact

        try:
            storage = get_artifact_storage()
            filepath = os.path.join(artifact.link.archive_path, artifact.output_path)

            storage.save(filepath, ContentFile(result.stdout))
            artifact.status = ArtifactStatus.SUCCEEDED
            success(f"Saved {self.plugin_name} to {filepath}", left_indent=4)
        except SuspiciousFileOperation as e:  # pragma: no coverage
            artifact.status = ArtifactStatus.FAILED
            error([f"{self.plugin_name} failed:", e])

        return artifact
