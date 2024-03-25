"""Functions to transform HTML to other formats."""

from copy import deepcopy
from functools import cached_property
from pathlib import Path
from typing import List, Optional, Protocol

from archeion.archivers import logger
from archeion.config import ArchiverSettings
from archeion.index.models import Artifact


class PostProcessorPlugin(Protocol):  # pragma: no cover
    """
    Interface for post-processing content from another artifact.

    All post-processor plugins should follow this interface.
    """

    plugin_name: str
    extracts_from_plugin: str

    def __init__(self, config: dict, *args, **kwargs): ...

    @cached_property
    def is_valid(self) -> bool:
        """Return True if the plugin is valid."""
        ...

    @cached_property
    def tool_name(self) -> str:
        """Return the tool name."""
        ...

    @cached_property
    def tool_version(self) -> str:
        """Return the tool version."""
        ...

    @cached_property
    def tool_binary(self) -> Optional[Path]:
        """Return the path to the tool."""
        ...

    async def __call__(self, artifact: Artifact, overwrite: bool = False) -> Artifact:
        """Archive the link."""
        ...


def get_all_post_processors() -> List[ArchiverSettings]:
    """Return a list of available post-processors."""
    import importlib

    from django.conf import settings

    plugins = []

    for archiver in settings.POST_PROCESSORS:
        plugin_info = deepcopy(archiver)
        module, class_name = plugin_info.class_path.rsplit(".", 1)
        try:
            if not archiver.enabled:
                plugin_info = disable_plugin(plugin_info, class_name)
            else:
                plugin_class = getattr(importlib.import_module(module), class_name)
                plugin_info.klass = plugin_class(config=archiver.dict())
                plugin_info.name = plugin_class.plugin_name
        except (ImportError, AttributeError) as e:
            logger.error(f"Unable to load archiver plugin {class_name}: {e}")
            plugin_info = disable_plugin(plugin_info, class_name)
        plugins.append(plugin_info)

    return plugins


def disable_plugin(plugin_info: ArchiverSettings, class_name: str) -> ArchiverSettings:
    """Disable a plugin."""
    plugin_info.enabled = False
    plugin_info.name = class_name
    plugin_info.klass = None
    return plugin_info


def get_post_processors_map() -> dict:
    """Return a map of available archivers."""
    return {plugin.name: plugin.klass for plugin in get_all_post_processors()}


def get_default_archivers() -> List[PostProcessorPlugin]:
    """Return just the default Archivers."""
    return [info.klass for info in get_all_post_processors() if info.enabled]
