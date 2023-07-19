"""Save the headers from accessing the link."""
import json
import os

from django.core.files.base import ContentFile
from seleniumwire.webdriver import Remote

from archeion.archivers.webdriver import WebDriverArchiver
from archeion.index.models import Artifact, ArtifactStatus
from archeion.index.storage import save_artifact_file
from archeion.logging import info
from archeion.utils import normalize_url


class HeadersArchiver(WebDriverArchiver):
    """Save the headers from accessing the link."""

    plugin_name = "headers"

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
        artifact.output_path = self.config.get("path", "headers.json")

        url = normalize_url(driver.current_url)
        headers: dict = {"url": url, "request_headers": {}, "response_headers": {}}

        for request in driver.requests:
            if request.url != url:
                continue
            headers["request_headers"].update(request.headers)
            if hasattr(request.response, "status_code"):
                headers["response_headers"]["status-code"] = request.response.status_code
            if hasattr(request.response, "headers"):
                headers["response_headers"].update(request.response.headers)

        filepath = os.path.join(artifact.link.archive_path, artifact.output_path)
        content = ContentFile(json.dumps(headers, indent=2))
        successful = save_artifact_file(filepath, content, self.plugin_name)
        artifact.status = ArtifactStatus.SUCCEEDED if successful else ArtifactStatus.FAILED

        return artifact
