"""Admin classes for the index app."""
from typing import Any, List

from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from ..logging import format_size_in_bytes
from .models import Artifact, Link, Tag


class ArtifactInline(admin.TabularInline):
    """Show the artifacts in the Link detail view."""

    model = Artifact


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin View for Tag.
    """

    list_display = [
        "name_with_sub",
    ]
    ordering = ["name"]
    raw_id_fields = ["substitute"]

    @admin.display(description=_("Name"), ordering="name")
    def name_with_sub(self) -> Any:
        """
        Render the name, or name with indication what its substitute is.
        """
        if self.substitute:
            return f"{self.name} &rarr; {self.substitute}"
        elif not self.enabled:
            return mark_safe(f'<span style="text-decoration: line-through">{self.name}</span>')  # nosec B308, B703
        else:
            return self.name


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    """
    Admin View for Link.
    """

    list_display: List[str] = [
        "__str__",
        "content_type",
        "ld_type",
        "archive_size_display",
        "created_at",
        "updated_at",
    ]
    list_editable: List[str] = []
    list_filter: List[str] = ["content_type", "ld_type", "created_at", "updated_at"]
    list_select_related: List[str] = []
    ordering: List[str] = ["-created_at"]
    raw_id_fields: List[str] = []
    readonly_fields: List[str] = []
    search_fields: List[str] = ["title"]
    actions = [
        "add_tags",
        "remove_tags",
        "update_titles",
        "update_snapshots",
        "resnapshot_snapshot",
        "overwrite_snapshots",
        "delete_snapshots",
    ]
    inlines = [ArtifactInline]
    list_per_page = settings.ITEMS_PER_PAGE

    @admin.display(description=_("archive_size"))
    def archive_size_display(self, obj):
        return format_size_in_bytes(obj.archive_size)


@admin.register(Artifact)
class ArtifactAdmin(admin.ModelAdmin):
    """
    Admin View for Artifact.
    """

    list_display = ("id", "plugin_name", "link", "status", "output_path_link")
    sort_fields = ("start_ts", "plugin_name", "status")
    readonly_fields = ("id", "link", "plugin_name", "output_path", "status", "start_ts", "end_ts")
    search_fields = (
        "id",
        "link__url",
        "plugin_name",
    )
    fields = readonly_fields

    list_filter = (
        "status",
        "plugin_name",
        "start_ts",
    )
    ordering = ["-start_ts"]
    list_per_page = settings.ITEMS_PER_PAGE

    @admin.display(description=_("output"), ordering="output_path")
    def output_path_link(self, obj: Artifact) -> Any:
        """Return the output path as a link."""
        if obj.output_path:
            return format_html(
                '<a href="{}" class="output-link">{} ↗</a>',
                mark_safe(obj.archive_output_path),  # nosec B308, B703
                obj.output_path,
            )
        else:
            return "No output"
