"""Archive a link using wget."""
from functools import cached_property
from pathlib import Path
from typing import Optional

from django.conf import settings
from django.utils import timezone

from archeion.dependency import bin_path, run_shell
from archeion.index.models import Artifact, ArtifactStatus
from archeion.logging import error


class WgetArchiver:
    """
    Download the link using wget.

    WGET CLI Docs: https://www.gnu.org/software/wget/manual/wget.html
    """

    plugin_name = "wget"

    def __init__(self, config: dict):
        """Initialize the plugin."""
        self.config = config
        self.args = config.get(
            "args",
            [
                "--no-verbose",
                "--adjust-extension",
                "--convert-links",
                "--force-directories",
                "--span-hosts",
                "--no-parent",
            ],
        )
        self.args.extend(
            [
                f"--timeout={settings.COMMAND_TIMEOUT}",
                "--restrict-file-names=windows",
                "--page-requisites",
                "--compression=auto",
            ]
        )
        if not settings.CHECK_SSL_VALIDITY:
            self.args.extend(["--no-check-certificate", "--no-hsts"])

        if self.config.get("save_directories", True):
            self.args.append(f"--directory-prefix={self.config.get('directories_path', 'wget/')}")

        if self.config.get("save_warc", True):
            self.args.append("--warc-cdx")

    @cached_property
    def is_valid(self) -> bool:
        """Make sure the requested WebDriver is installed and ready."""
        return self.tool_version != "(Not available)"

    @cached_property
    def tool_name(self) -> str:
        """Return the tool name."""
        return "Wget"

    @cached_property
    def tool_version(self) -> str:
        """Return the tool version."""
        import re

        result = run_shell([str(self.tool_binary), "--version"])

        match = re.search(r"GNU Wget (\d+\.\d+\.\d+)", result.stdout)
        if result.returncode != 0 or not match:
            return "(Not available)"

        return match.group(1)

    @cached_property
    def tool_binary(self) -> Optional[Path]:
        """Return the path to the tool."""
        return Path(bin_path("wget"))

    async def __call__(self, artifact: Artifact, overwrite: bool = False) -> Artifact:
        """
        Download the link using Selenium WebDriver.

        Args:
            artifact: The to process
            overwrite: Overwrite the file if it already exists

        Returns:
            The modified artifact
        """
        if artifact.status == ArtifactStatus.SUCCEEDED and not overwrite:
            return artifact

        if not self.is_valid:
            artifact.status = ArtifactStatus.FAILED
            error(f"{self.plugin_name} is not valid.")
            return artifact

        artifact.start_ts = timezone.now()

        if self.config.get("save_warc", True):
            self.args.append(f"--warc-file={artifact.link_id}")

        cmd = [self.tool_binary, *self.args, artifact.link.url]

        result = run_shell(cmd, cwd=str(artifact.archive_output_path))

        # parse out number of files downloaded from last line of stderr:
        #  "Downloaded: 76 files, 4.0M in 1.6s (2.52 MB/s)"
        output_tail = [
            line.strip() for line in (result.stdout + result.stderr).decode().rsplit("\n", 3)[-3:] if line.strip()
        ]
        files_downloaded = (
            int(output_tail[-1].strip().split(" ", 2)[1] or 0) if "Downloaded:" in output_tail[-1] else 0
        )
        hints = (
            f"Got wget response code: {result.returncode}.",
            *output_tail,
        )
        artifact.status = ArtifactStatus.SUCCEEDED

        # Check for common failure cases
        if result.returncode > 0 and files_downloaded < 1:
            artifact.status = ArtifactStatus.FAILED
            if "403: Forbidden" in result.stderr:
                error(["403 Forbidden (try changing WGET_USER_AGENT)", *hints])
            if "404: Not Found" in result.stderr:
                error(["404 Not Found", *hints])
            if "ERROR 500: Internal Server Error" in result.stderr:
                error(["500 Internal Server Error", *hints])
            error(["Wget failed or got an error from the server", *hints])

        artifact.end_ts = timezone.now()

        return artifact
