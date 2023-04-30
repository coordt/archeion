"""Download the DOM of the link."""
import os

from django.core.exceptions import SuspiciousFileOperation
from django.core.files.base import ContentFile
from selenium.webdriver import Remote

from archeion.archivers.webdriver import WebDriverArchiver
from archeion.index.models import Artifact, ArtifactStatus
from archeion.index.storage import get_artifact_storage
from archeion.logging import error, info, success


class DOMArchiver(WebDriverArchiver):
    """Download the DOM of the link."""

    plugin_name = "DOM"

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
        artifact.output_path = self.config.get("path", "dom.html")

        try:
            storage = get_artifact_storage()
            filepath = os.path.join(artifact.link.archive_path, artifact.output_path)
            storage.save(filepath, ContentFile(driver.page_source))
            artifact.status = ArtifactStatus.SUCCEEDED
            success(f"Saved {self.plugin_name} to {filepath}", left_indent=4)
        except SuspiciousFileOperation as e:  # pragma: no coverage
            artifact.status = ArtifactStatus.FAILED
            error([f"{self.plugin_name} failed:", e])

        return artifact
