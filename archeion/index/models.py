"""Models for keeping track of links and the artifacts generated from them."""
import os
from typing import Any
from urllib.parse import urlparse

import httpx
from django.core.cache import cache
from django.db import models
from django.db.models import F
from django.db.models.signals import m2m_changed
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from shortuuid.django_fields import ShortUUIDField

from archeion.index.storage import get_artifact_storage
from archeion.utils import IterableEncoder, get_dir_size, model_slugify


class Tag(models.Model):
    """
    A tag on a link.
    """

    id = ShortUUIDField(
        _("id"),
        null=False,
        blank=False,
        editable=False,
        primary_key=True,
    )
    name = models.CharField(_("name"), max_length=200, null=False, blank=False, help_text=_("The tag"))
    slug = AutoSlugField(
        _("slug"),
        populate_from="name",
        max_length=200,
        slugify_function=model_slugify,
    )
    enabled = models.BooleanField(
        _("enabled"),
        null=False,
        blank=False,
        default=True,
        help_text=_("If False, it will remove current associations and will not allow new associations."),
    )
    substitute = models.ForeignKey(
        "self",
        verbose_name=_("substitute"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text=_(
            "Tag to use instead of this one. Moves current "
            "associations to the substitute tag and new association attempts "
            "are automatically swapped."
        ),
    )

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        ordering = ["name"]

    def __str__(self):
        """Return the name of the tag."""
        return self.name

    def save(self, *args, **kwargs) -> None:
        """Manage the substitutions and enable/disable the tag."""
        super().save(*args, **kwargs)
        if self.substitute:
            items = self.links.through.objects.all()
            items.update(tag=self.substitute)
        if not self.enabled:
            self.links.all().delete()


class Link(models.Model):
    """
    A link to a URL to archive.
    """

    id = ShortUUIDField(
        _("id"),
        null=False,
        blank=False,
        editable=False,
        primary_key=True,
    )
    url = models.URLField(
        _("url"),
        max_length=200,
        null=False,
        blank=False,
        help_text=_("The URL to archive."),
    )
    parsed_url = models.JSONField(
        _("parsed url"), null=False, blank=False, help_text=_("The URL parsed into its components.")
    )
    archive_path = models.CharField(
        _("archive path"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("The path relative to the archive root to store artifacts."),
    )
    content_type = models.CharField(
        _("content type"), max_length=100, null=True, blank=True, help_text=_("The content type of the URL.")
    )

    title = models.CharField(
        _("title"), max_length=255, null=True, blank=True, help_text=_("The title of the linked resource.")
    )
    favicon_url = models.CharField(
        _("favicon url"),
        max_length=200,
        null=True,
        blank=True,
        default="",
        help_text=_("The URL to the site's favicon"),
    )
    ld_type = models.CharField(
        _("Linked data type"),
        max_length=200,
        null=True,
        blank=True,
        help_text=_("The Linked Data type from Schema.org"),
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_("tags"),
        related_name="links",
        help_text=_("Tags applied to the link."),
    )
    metadata = models.JSONField(
        _("metadata"), encoder=IterableEncoder, null=False, blank=True, default=dict, help_text=_("Metadata ")
    )
    created_at = models.DateTimeField(
        _("created at"),
        null=False,
        blank=False,
        auto_now_add=True,
        editable=False,
        help_text=_("The date and time this tag was created."),
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        null=False,
        blank=False,
        editable=False,
        auto_now=True,
        help_text=_("The date and time this tag was last updated."),
    )

    class Meta:
        verbose_name = _("Link")
        verbose_name_plural = _("Links")
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title or self.url

    def get_absolute_url(self) -> str:
        """Return the absolute URL of the link."""
        return reverse("link-detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs) -> None:
        """
        Describe why you are overriding the save method here.
        """
        if not self.parsed_url:
            self.parsed_url = urlparse(self.url)

        if self.content_type is None:
            result = httpx.head(self.url, follow_redirects=True)
            self.content_type = result.headers["Content-Type"] if result.status_code == 200 else None

        if not self.archive_path:
            self.archive_path = self.id

        if self.metadata and not isinstance(self.metadata, dict):
            self.metadata = {"unknown": self.metadata}

        if not self.favicon_url:
            self.favicon_url = f"https://www.google.com/s2/favicons?domain={self.parsed_url.netloc}"

        super().save(*args, **kwargs)

    @cached_property
    def archive_size(self) -> int:
        """Calculate the total amount of storage taken up by the archive."""
        cache_key = f"{str(self.id)[:12]}-{(self.updated_at or self.created_at).timestamp()}-size"

        def calc_dir_size() -> int:
            return get_dir_size(storage=get_artifact_storage(), path=self.archive_path)

        return cache.get_or_set(cache_key, calc_dir_size)

    def update_metadata(self, new_metadata: dict) -> None:
        """Update the link's metadata."""
        metadata = self.metadata or {}
        metadata.update(new_metadata)

        # Create the tags and add the tags to the link.tags
        for tag_name in metadata.get("keywords", []):
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            self.tags.add(tag)

        if not self.ld_type and "type" in metadata:
            self.ld_type = metadata.get("type", None)

        if not self.title and "headline" in metadata:
            self.title = metadata["headline"][:255]


class ArtifactStatus(models.TextChoices):
    """Status choices for Artifacts."""

    PENDING = "pending", _("Pending")
    SUCCEEDED = "succeeded", _("succeeded")
    FAILED = "failed", _("failed")
    SKIPPED = "skipped", _("skipped")


class Artifact(models.Model):
    """
    An archived artifact.
    """

    id = ShortUUIDField(
        _("id"),
        null=False,
        blank=False,
        editable=False,
        primary_key=True,
    )
    link = models.ForeignKey(
        Link,
        verbose_name=_("link"),
        related_name="artifacts",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        help_text=_("The link used to archive this artifact."),
    )
    extracted_from = models.ForeignKey(
        "self",
        verbose_name=_("extracted from"),
        related_name="extractions",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"link": F("link")},
        help_text=_("The artifact used to extract this artifact."),
    )

    plugin_name = models.CharField(
        _("plugin name"),
        max_length=32,
        null=False,
        blank=False,
        help_text=_("The name of the plugin used generate this artifact."),
    )
    output_path = models.CharField(
        _("output path"),
        max_length=200,
        null=True,
        blank=True,
        default="",
        help_text=_("The path, relative to the link's archive_path, to the archived result."),
    )
    status = models.CharField(
        _("status"),
        max_length=32,
        null=False,
        blank=True,
        default=ArtifactStatus.PENDING,
        help_text=_("The status of the archive process."),
    )
    start_ts = models.DateTimeField(
        _("start timestamp"), null=True, blank=True, help_text=_("The start time of the archive process.")
    )
    end_ts = models.DateTimeField(
        _("end timestamp"), null=True, blank=True, help_text=_("The end time of the archive process.")
    )

    class Meta:
        verbose_name = _("Artifact")
        verbose_name_plural = _("Artifacts")
        get_latest_by = "start_ts"
        order_with_respect_to = "link"
        constraints = [models.UniqueConstraint(fields=["link", "plugin_name"], name="unique_link_plugin_name")]

    def __str__(self) -> str:
        return self.plugin_name

    def get_absolute_url(self) -> str:
        """Return the absolute URL of the artifact."""
        return reverse("artifact-detail", kwargs={"link_id": self.link_id, "slug": self.plugin_name})

    @property
    def archive_output_path(self) -> str:
        """Return the full path to the output file."""
        return os.path.join(self.link.archive_path, self.output_path)


def m2m_save_listener(
    sender: models.Model, instance: Any, action: str, reverse: bool, model: Any, pk_set: set, using: str, **kwargs
) -> None:
    """This does the substitution of tags when added by a link."""
    if action == "pre_add" and not reverse:
        sub_ids = model.objects.filter(pk__in=pk_set).exclude(substitute_id=None).values_list("id", "substitute_id")
        for tag_id, substitute_id in sub_ids:
            pk_set.remove(tag_id)
            pk_set.add(substitute_id)
        disabled_ids = model.objects.filter(pk__in=pk_set, enabled=False).values_list("id", flat=True)
        for tag_id in disabled_ids:
            pk_set.remove(tag_id)


m2m_changed.connect(m2m_save_listener, sender=Link.tags.through)
