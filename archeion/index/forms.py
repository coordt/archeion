"""Forms for user input and validation."""
from django import forms

from archeion.archivers import get_archivers_map

ARCHIVER_CHOICES = [(item, item) for item in get_archivers_map().keys()]


class AddLinkForm(forms.Form):
    """Add a link to the archive with this form."""

    url = forms.URLField(label="URL", min_length="6", required=True)
    archive_methods = forms.MultipleChoiceField(
        label="Archive methods",
        required=False,
        choices=ARCHIVER_CHOICES,
        initial=get_archivers_map().keys(),
    )
    # TODO: hook these up to the view and put them
    # in a collapsible UI section labeled "Advanced"
    #
    # exclude_patterns = forms.CharField(
    #     label="Exclude patterns",
    #     min_length='1',
    #     required=False,
    #     initial=URL_BLACKLIST,
    # )
    # timeout = forms.IntegerField(
    #     initial=TIMEOUT,
    # )
    # overwrite = forms.BooleanField(
    #     label="Overwrite any existing Snapshots",
    #     initial=False,
    # )
    # index_only = forms.BooleanField(
    #     label="Add URLs to index without Snapshotting",
    #     initial=False,
    # )
