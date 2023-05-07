"""Tables for listing the models in HTML."""
from typing import Any

import django_filters
import django_tables2 as tables
from crispy_forms.helper import FormHelper

from .models import Link


class FilterFormHelper(FormHelper):
    """Helper for the FilterForm."""

    form_method = "GET"
    field_template = "bootstrap5/layout/inline_field.html"
    form_tag = False


class LinkFilter(django_filters.FilterSet):
    """Filters for the Link table."""

    content_type = django_filters.AllValuesFilter(field_name="content_type")
    ld_type = django_filters.AllValuesFilter(field_name="ld_type")
    created_at = django_filters.DateRangeFilter()

    class Meta:
        model = Link
        fields = ["content_type", "ld_type", "created_at"]


class LinkTable(tables.Table):
    """Table definiton for the Link table."""

    url = tables.LinkColumn(empty_values=())

    class Meta:
        model = Link
        template_name = "django_tables2/bootstrap5.html"
        fields = ("url", "ld_type", "created_at")
        attrs = {
            "class": "table table-striped table-bordered",
            # "thead": {"class": "table-light"},
        }

    def render_url(self, value: Any, record: Link) -> str:
        """Return the value to render for the URL column."""
        return record.title or str(value)
