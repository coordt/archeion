"""Save a PDF of the link."""
import base64
import os

from django.core.exceptions import SuspiciousFileOperation
from django.core.files.base import ContentFile
from selenium.webdriver import Remote

from archeion.archivers.webdriver import WebDriverArchiver
from archeion.index.models import Artifact, ArtifactStatus
from archeion.index.storage import get_artifact_storage
from archeion.logging import error, info, success

WINDOW_UI_HEIGHT = 156
"""The height of the window UI. This is used to calculate the height of the screenshot."""


class PDFArchiver(WebDriverArchiver):
    """Save a PDF of the link."""

    plugin_name = "PDF"

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
        info(f"Saving {self.plugin_name}...")
        artifact.output_path = self.config.get("path", "print.pdf")
        try:
            storage = get_artifact_storage()
            filepath = os.path.join(artifact.link.archive_path, artifact.output_path)
            b64_encoded_pdf = driver.print_page()
            storage.save(filepath, ContentFile(base64.b64decode(b64_encoded_pdf)))
            artifact.status = ArtifactStatus.SUCCEEDED
            success(f"Saved {self.plugin_name} to {filepath}")
        except SuspiciousFileOperation as e:  # pragma: no coverage
            artifact.status = ArtifactStatus.FAILED
            error([f"{self.plugin_name} failed:", e])

        return artifact
