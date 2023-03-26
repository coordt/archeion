"""Download a link using Selenium WebDriver."""
from pathlib import Path
from typing import Optional

import selenium
from distlib.util import cached_property
from django.utils import timezone
from selenium.common import WebDriverException
from selenium.webdriver import Remote
from seleniumwire.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

from archeion.index.models import Artifact, ArtifactStatus
from archeion.logging import error, info


class WebDriverArchiver:
    """
    Download the link using Selenium WebDriver.
    """

    plugin_name = "webdriver"

    def __init__(self, config: dict):
        """Initialize the plugin."""
        self.args = config.get("args", ["--headless"])
        self.driver = Chrome
        self.options = ChromeOptions()
        for arg in self.args:
            self.options.add_argument(arg)
        self.exec_path = ChromeDriverManager().install()
        self.config = config

    @cached_property
    def is_valid(self) -> bool:
        """Make sure the requested WebDriver is installed and ready."""
        try:
            with self.driver(self.exec_path, options=self.options):
                return True
        except WebDriverException:
            return False

    @cached_property
    def tool_name(self) -> str:
        """Return the tool name."""
        return "Selenium WebDriver (Chrome)"

    @cached_property
    def tool_version(self) -> str:
        """Return the tool version."""
        if not self.is_valid:
            return f"{selenium.__version__} (Not installed)"

        with self.driver(self.exec_path, options=self.options) as driver:
            return f"{selenium.__version__} ({driver.caps['browserVersion']})"

    @cached_property
    def tool_binary(self) -> Optional[Path]:
        """Return the path to the tool."""
        return Path(self.exec_path) if self.is_valid else None

    async def save_artifact(self, driver: Remote, artifact: Artifact) -> Artifact:
        """
        Save the artifact.

        This method will always overwrite the existing artifact.

        # noqa: DAR202

        Args:
            driver: The Selenium WebDriver instance.
            artifact: The Artifact model instance.

        Raises:
            NotImplementedError: if a subclass doesn't implement it

        Returns:
            The modified Artifact record.
        """
        raise NotImplementedError

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
        info(f"{self.plugin_name}: Downloading {artifact.link.url}...", left_indent=4)
        with self.driver(self.exec_path, options=self.options) as driver:  # pragma: no-cover
            driver.implicitly_wait(10)  # seconds
            driver.get(artifact.link.url)
            artifact = await self.save_artifact(driver, artifact)

        artifact.end_ts = timezone.now()
        return artifact
