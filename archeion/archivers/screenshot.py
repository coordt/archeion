"""Save a screenshot of the link."""
import os
import subprocess

from django.core.exceptions import SuspiciousFileOperation
from django.core.files.base import ContentFile
from selenium.webdriver import Remote

from archeion.archivers.webdriver import WebDriverArchiver
from archeion.index.models import Artifact, ArtifactStatus
from archeion.index.storage import get_artifact_storage
from archeion.logging import error, info, success

WINDOW_UI_HEIGHT = 156
"""The height of the window UI. This is used to calculate the height of the screenshot."""


def optimize_png(img_data: bytes) -> bytes:
    # TODO: Add pngquant to dependency checker and use existing functions.
    cmd = ["pngquant", "--strip", "--quality", "70-95", "-"]
    result = subprocess.run(cmd, input=img_data, capture_output=True)
    return result.stdout if len(img_data) > len(result.stdout) else img_data


class ScreenshotArchiver(WebDriverArchiver):
    """Save a screenshot of the link."""

    plugin_name = "screenshot"

    async def save_artifact(self, driver: Remote, artifact: Artifact) -> Artifact:
        """
        Save the artifact.

        This method will always overwrite the existing artifact.

        Args:
            driver: The Selenium WebDriver instance.
            artifact: The Artifact record to modify.

        Returns:
            The modified Artifact record.
        """
        info(f"Saving {self.plugin_name}...", left_indent=4)
        artifact.output_path = self.config.get("path", "screenshot.png")
        width, height = self.config.get("resolution", (1440, 2000))
        driver.set_window_size(width, height + WINDOW_UI_HEIGHT)
        try:
            storage = get_artifact_storage()
            filepath = os.path.join(artifact.link.archive_path, artifact.output_path)
            img_data = optimize_png(driver.get_screenshot_as_png())
            storage.save(filepath, ContentFile(img_data))
            artifact.status = ArtifactStatus.SUCCEEDED
            success(f"Saved {self.plugin_name} to {filepath}", left_indent=4)
        except SuspiciousFileOperation as e:  # pragma: no coverage
            artifact.status = ArtifactStatus.FAILED
            error([f"{self.plugin_name} failed:", e])

        return artifact
