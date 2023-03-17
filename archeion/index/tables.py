"""Tables for listing the models in HTML."""
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

    created_at = django_filters.DateFromToRangeFilter()

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

    def render_url(self, value, record):
        """Return the value to render for the URL column."""
        return record.title or value
