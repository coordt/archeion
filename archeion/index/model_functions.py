"""Functions that provide service to one or more models."""
from archeion.index.models import ArtifactStatus, Link
from archeion.index.storage import get_artifact_storage


def save_link_data(obj: Link) -> None:
    """Serialize a link record into a YAML file."""
    from io import StringIO

    import yaml
    from django.core.serializers.python import Serializer

    try:
        from yaml import CSafeDumper as SafeDumper
    except ImportError:
        from yaml import SafeDumper  # type: ignore[assignment]

    serializer = Serializer()
    serializer.use_natural_foreign_keys = False
    serializer.use_natural_primary_keys = False

    selected_fields = None
    concrete_model = obj._meta.concrete_model
    serializer.start_object(obj)
    for field in concrete_model._meta.local_fields:
        if field.serialize:
            if field.remote_field is None:
                if selected_fields is None or field.attname in serializer.selected_fields:
                    serializer.handle_field(obj, field)
            elif selected_fields is None or field.attname[:-3] in serializer.selected_fields:
                serializer.handle_fk_field(obj, field)
    for field in concrete_model._meta.local_many_to_many:
        if (selected_fields is None or field.attname in serializer.selected_fields) and field.serialize:
            serializer.handle_m2m_field(obj, field)

    data = serializer._current
    data["id"] = obj.id
    data["parsed_url"] = tuple(obj.parsed_url)
    data["tags"] = [tag.name for tag in obj.tags.all()]
    stream = StringIO()
    yaml.dump(data, stream, Dumper=SafeDumper, allow_unicode=True)
    storage = get_artifact_storage()
    filename = f"{obj.archive_path}/index.yaml"
    if storage.exists(filename):
        storage.delete(filename)
    storage.save(filename, stream)


def index_link_data(link: Link) -> None:
    """Index the link data."""
    from io import StringIO

    from archeion.search import index

    artifacts = link.artifacts.filter(status=ArtifactStatus.SUCCEEDED).filter(
        plugin_name__in=("DOM", "headers", "html_metadata", "markdown")
    )
    artifact_map = {artifact.plugin_name: artifact for artifact in artifacts}
    content = StringIO()
    content.write(f"{link.title or ''}\n")
    tags = link.tags.values_list("name", flat=True)
    if tags:
        content.write(f"Tags: {', '.join(tags)}\n")
    content.write(f"URL: {link.url}\n")
    if "html_metadata" in artifact_map:
        content.write(f"{artifact_map['html_metadata'].content}\n")
    if "markdown" in artifact_map:
        content.write(f"{artifact_map['markdown'].content}\n")
    elif "DOM" in artifact_map:
        content.write(f"{artifact_map['DOM'].content}\n")

    index(link.id, content.getvalue())
