import shutil
from itertools import chain
from pathlib import Path
from typing import List

from django.conf import settings

from archeion.logging import error

DEFAULT_IGNORE_EXTENSIONS = ("css", "js", "orig", "svg")

DEFAULT_ARGUMENTS = [
    "--ignore-case",
    "--files-with-matches",
]


class RipGrepBackend:
    """A search engine backend that uses ripgrep (rg)."""

    def __init__(self, config: dict):
        if not self.is_valid():
            raise RuntimeError("ripgrep (rg) binary not found, install ripgrep to use this search backend.")

        self.config = config
        ignore_extensions = config.get("ignore_extensions", DEFAULT_IGNORE_EXTENSIONS)
        default_args = config.get("default_arguments", DEFAULT_ARGUMENTS)
        ignore_args = list(
            chain.from_iterable(
                zip(["--iglob"] * len(ignore_extensions), [f"'!*.{ext}'" for ext in ignore_extensions])
            )
        )
        self.rg_command = ["rg", *ignore_args, *default_args]
        self.timeout = int(config.get("timeout", 90))

    @classmethod
    def is_valid(cls) -> bool:
        """Is the backend ready to go?"""
        return bool(shutil.which("rg"))

    def index_link(self, link_id: str, tags: List[str]) -> None:
        """
        Index the tags for the link_id.
        """
        return

    def index_artifact(self, artifact_id: str, link_id: str, content: str) -> None:
        """Index the content for an artifact/link combination."""
        return

    def search(self, query: str) -> List[str]:
        from archeion.dependency import run_shell

        rg_cmd = [*self.rg_command, "-e", query, str(settings.ARTIFACTS_DIR_NAME)]

        result = run_shell(rg_cmd, cwd=settings.ARTIFACTS_DIR_NAME)
        if result.returncode != 0:
            error([f"ripgrep returned non-zero exit code: {result.returncode}", result.stderr])
            return []

        file_paths = result.stdout.splitlines()
        link_ids = set()
        for path in file_paths:
            rel_path = Path(path).relative_to(settings.ARTIFACTS_DIR_NAME)
            link_ids.add(rel_path.parents[-2].name)  # .parents[-1] is "."

        return list(link_ids)
