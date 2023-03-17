"""Admin classes for the index app."""
from typing import List

from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

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
    def name_with_sub(self):
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

    list_display: List[str] = ["__str__", "content_type", "ld_type", "archive_size", "created_at", "updated_at"]
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

    # def grid_view(self, request, extra_context=None):
    #
    #     # cl = self.get_changelist_instance(request)
    #
    #     # Save before monkey patching to restore for changelist list view
    #     saved_change_list_template = self.change_list_template
    #     saved_list_per_page = self.list_per_page
    #     saved_list_max_show_all = self.list_max_show_all
    #
    #     # Monkey patch here plus core_tags.py
    #     self.change_list_template = "private_index_grid.html"
    #     self.list_per_page = settings.LIST_PER_PAGE
    #     self.list_max_show_all = self.list_per_page
    #
    #     # Call monkey patched view
    #     rendered_response = self.changelist_view(request, extra_context=extra_context)
    #
    #     # Restore values
    #     self.change_list_template = saved_change_list_template
    #     self.list_per_page = saved_list_per_page
    #     self.list_max_show_all = saved_list_max_show_all
    #
    #     return rendered_response

    # for debugging, uncomment this to print all requests:
    # def changelist_view(self, request, extra_context=None):
    #     print('[*] Got request', request.method, request.POST)
    #     return super().changelist_view(request, extra_context=None)

    # def update_snapshots(self, request, queryset):
    #     archive_links([snapshot.as_link() for snapshot in queryset], out_dir=OUTPUT_DIR)
    #
    # update_snapshots.short_description = "Pull"

    # def update_titles(self, request, queryset):
    #     archive_links(
    #         [snapshot.as_link() for snapshot in queryset],
    #         overwrite=True,
    #         methods=("title", "favicon"),
    #         out_dir=OUTPUT_DIR,
    #     )
    #
    # update_titles.short_description = "⬇️ Title"

    # def resnapshot_snapshot(self, request, queryset):
    #     for snapshot in queryset:
    #         timestamp = datetime.now(timezone.utc).isoformat("T", "seconds")
    #         new_url = snapshot.url.split("#")[0] + f"#{timestamp}"
    #         add(new_url, tag=snapshot.tags_str())
    #
    # resnapshot_snapshot.short_description = "Re-Snapshot"

    # def overwrite_snapshots(self, request, queryset):
    #     archive_links([snapshot.as_link() for snapshot in queryset], overwrite=True, out_dir=OUTPUT_DIR)
    #
    # overwrite_snapshots.short_description = "Reset"

    # def delete_snapshots(self, request, queryset):
    #     remove(snapshots=queryset, yes=True, delete=True, out_dir=OUTPUT_DIR)
    #
    # delete_snapshots.short_description = "Delete"

    # def add_tags(self, request, queryset):
    #     tags = request.POST.getlist("tags")
    #     print("[+] Adding tags", tags, "to Snapshots", queryset)
    #     for obj in queryset:
    #         obj.tags.add(*tags)
    #
    # add_tags.short_description = "+"
    #
    # def remove_tags(self, request, queryset):
    #     tags = request.POST.getlist("tags")
    #     print("[-] Removing tags", tags, "to Snapshots", queryset)
    #     for obj in queryset:
    #         obj.tags.remove(*tags)
    #
    # remove_tags.short_description = "–"


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
    def output_path_link(self, obj: Artifact):
        """Return the output path as a link."""
        if obj.output_path:
            return format_html(
                '<a href="{}" class="output-link">{} ↗</a>',
                mark_safe(obj.archive_output_path),  # nosec B308, B703
                obj.output_path,
            )
        else:
            return "No output"
