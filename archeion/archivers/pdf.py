"""Save a PDF of the link."""

import base64
import os

from django.core.files.base import ContentFile
from selenium.webdriver import Remote

from archeion.archivers.webdriver import WebDriverArchiver
from archeion.exceptions import ArchiverError
from archeion.index.models import Artifact, ArtifactStatus
from archeion.index.storage import save_artifact_file
from archeion.logging import info

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

        Raises:
            ArchiverError: If the PDF could not be saved.
        """
        info(f"Saving {self.plugin_name}...", left_indent=4)
        artifact.output_path = self.config.get("path", "print.pdf")

        b64_encoded_pdf = driver.print_page()
        if not b64_encoded_pdf:
            raise ArchiverError("Failed to get PDF.")

        filepath = os.path.join(artifact.link.archive_path, artifact.output_path)
        content = ContentFile(base64.b64decode(b64_encoded_pdf))
        successful = save_artifact_file(filepath, content, self.plugin_name)
        artifact.status = ArtifactStatus.SUCCEEDED if successful else ArtifactStatus.FAILED

        return artifact
