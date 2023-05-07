"""Download content from YouTube."""
from pathlib import Path
from typing import Optional

from distlib.util import cached_property
from django.conf import settings
from django.utils import timezone

from archeion.dependency import bin_path, run_shell
from archeion.index.models import Artifact, ArtifactStatus
from archeion.logging import error


class YouTubeDLArchiver:
    """
    Download content from YouTube.
    """

    plugin_name = "youtube-dl"

    def __init__(self, config: dict):
        """Initialize the plugin."""
        self.args = config.get("args", [])
        if not settings.CHECK_SSL_VALIDITY:
            self.args.append("--no-check-certificate")
        self.max_filesize = config.get("max_filesize", "750m")
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
            self.save_media(artifact.link.url, artifact.archive_output_path)
            artifact.status = ArtifactStatus.SUCCEEDED
        except RuntimeError:
            artifact.status = ArtifactStatus.FAILED

        artifact.end_ts = timezone.now()
        return artifact

    def save_media(self, url: str, destination: Path):
        """Download playlists or individual video, audio, and subtitles using youtube-dl."""
        destination.mkdir(exist_ok=True)
        cmd = [
            self.tool_binary,
            *self.args,
            # TODO: add --cookies-from-browser={CHROME_USER_DATA_DIR}
            url,
        ]
        result = run_shell(cmd, cwd=destination)
        if result.returncode:
            if (
                "ERROR: Unsupported URL" in result.stderr
                or "HTTP Error 404" in result.stderr
                or "HTTP Error 403" in result.stderr
                or "URL could be a direct video link" in result.stderr
                or "Unable to extract container ID" in result.stderr
            ):
                # These happen too frequently on non-media pages to warrant printing to console
                return
            hints = (
                f"Got youtube-dl response code: {result.returncode}.",
                *result.stderr.split("\n"),
            )
            error(["Failed to save media", *hints])
            raise RuntimeError("Failed to save media.")
