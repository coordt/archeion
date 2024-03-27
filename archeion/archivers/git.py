"""Clone a git repo."""

import urllib.parse
from pathlib import Path
from typing import Optional

from distlib.util import cached_property
from django.conf import settings
from django.utils import timezone

from archeion.dependency import bin_path, run_shell
from archeion.index.models import Artifact, ArtifactStatus
from archeion.logging import error
from archeion.utils import normalize_url


class GitArchiver:
    """
    Clone a git repository.
    """

    plugin_name = "git"

    def __init__(self, config: dict):
        """Initialize the plugin."""
        self.args = config.get("args", [])
        self.domains = config.get("domains", ["github.com", "bitbucket.org", "gitlab.com", "gist.github.com"])
        if not settings.CHECK_SSL_VALIDITY:
            self.args.extend(["-c", "http.sslVerify=false"])
        self.config = config

    @cached_property
    def is_valid(self) -> bool:
        """Make sure the requested WebDriver is installed and ready."""
        return self.tool_version != "(Not available)"

    @cached_property
    def tool_name(self) -> str:
        """Return the tool name."""
        return "Git"

    @cached_property
    def tool_version(self) -> str:
        """Return the tool version."""
        import re

        result = run_shell([str(self.tool_binary), "--version"])

        match = re.search(r"git version (\d+\.\d+\.\d+)", result.stdout)
        if result.returncode != 0 or not match:
            return "(Not available)"

        return match.group(1)

    @cached_property
    def tool_binary(self) -> Optional[Path]:
        """Return the path to the tool."""
        return Path(bin_path("git"))

    def is_cloneable_url(self, url: str) -> bool:
        """Return ``True`` if git can clone it."""
        parts = urllib.parse.urlparse(url)
        return parts.netloc in self.domains or parts.path.endswith(".git")

    async def __call__(self, artifact: Artifact, overwrite: bool = False) -> Artifact:
        """
        Download the link using Selenium WebDriver.

        Args:
            artifact: The to process
            overwrite: Overwrite the file if it already exists

        Returns:
            The modified Artifact record.
        """
        if artifact.status == ArtifactStatus.SUCCEEDED and not overwrite:
            return artifact

        if not self.is_valid:
            artifact.status = ArtifactStatus.FAILED
            error(f"{self.plugin_name} is not valid.")
            return artifact

        artifact.start_ts = timezone.now()

        try:
            self.save_git(artifact.link.url, artifact.archive_output_path)
            artifact.status = ArtifactStatus.SUCCEEDED
        except RuntimeError:
            artifact.status = ArtifactStatus.FAILED

        artifact.end_ts = timezone.now()
        return artifact

    def save_git(self, url: str, destination: Path):
        """Clone a git repository."""
        normalized_url = normalize_url(url)
        destination.mkdir(exist_ok=True)
        cmd = [
            self.tool_binary,
            "clone",
            *self.args,
            normalized_url,
        ]
        result = run_shell(cmd, cwd=destination)

        if result.returncode == 128:
            # ignore failed re-download when the folder already exists
            return
        elif result.returncode > 0:
            hints = f"Got git response code: {result.returncode}."
            error(["Failed to save git clone", *hints])
            raise RuntimeError("Failed to save git repository.")
