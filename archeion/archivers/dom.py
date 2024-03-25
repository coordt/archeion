"""Download the DOM of the link."""

import os

from django.core.files.base import ContentFile
from selenium.webdriver import Remote

from archeion.archivers.webdriver import WebDriverArchiver
from archeion.index.models import Artifact, ArtifactStatus
from archeion.index.storage import save_artifact_file
from archeion.logging import info


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

        filepath = os.path.join(artifact.link.archive_path, artifact.output_path)
        content = ContentFile(driver.page_source)
        successful = save_artifact_file(filepath, content, self.plugin_name)
        artifact.status = ArtifactStatus.SUCCEEDED if successful else ArtifactStatus.FAILED

        return artifact
