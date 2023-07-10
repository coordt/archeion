from archeion.index.models import Artifact, Link


def get_existing_artifacts() -> dict:
    from collections import defaultdict

    artifacts = Artifact.objects.values_list("link_id", "plugin_name").order_by("link_id")
    artifact_map = defaultdict(set)
    for item in artifacts:
        artifact_map[item[0]].add(item[1])
    return artifact_map


def get_links_missing_artifacts() -> dict:
    """Get the link ids that are missing artifacts."""
    from archeion.archivers import get_all_archivers

    artifact_map = get_existing_artifacts()

    link_ids = Link.objects.values_list("id", flat=True)
    default_plugin_names = {plugin.name for plugin in get_all_archivers() if plugin.enabled}
    missing_artifacts_map = dict.fromkeys(link_ids, set())

    for link_id in missing_artifacts_map:
        missing_artifacts_map[link_id] = default_plugin_names - artifact_map.get(link_id, set())

    return missing_artifacts_map


def add_missing_artifacts():
    """Create Artifact records where Links are missing them."""
    for link_id, plugin_names in get_links_missing_artifacts().items():
        for plugin_name in plugin_names:
            Artifact.objects.create(link_id=link_id, plugin_name=plugin_name)


if __name__ == "__main__":
    get_links_missing_artifacts()
