"""External views for the index app."""
from typing import Any

from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, FormView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from archeion import __version__
from archeion.json2html import convert_json2html

# from archeion.search import query_search_index
from ..logging import info
from .forms import AddLinkForm
from .models import Artifact, Link
from .tables import FilterFormHelper, LinkFilter, LinkTable

HIDDEN_PLUGINS = {
    "title",
    "favicon",
}


class HomepageView(SingleTableMixin, FilterView):
    """Homepage view."""

    template_name = "index/links.html"
    model = Link
    table_class = LinkTable
    filterset_class = LinkFilter
    paginate_by = 20

    def get_context_data(self, **kwargs) -> Any:
        """Add additional information to the context."""
        context = super().get_context_data(**kwargs)
        context["filter_helper"] = FilterFormHelper
        return context


class LinkDetailView(DetailView):
    """Link detail view."""

    template_name = "index/link_detail.html"
    queryset = Link.objects.all().prefetch_related()

    def get_context_data(self, **kwargs) -> dict:
        """Add additional information to the context."""
        context = super().get_context_data(**kwargs)
        context["artifacts"] = {}
        for artifact in self.object.artifacts.all():
            context["artifacts"][artifact.plugin_name] = artifact
        if self.object.metadata:
            context["metadata"] = mark_safe(convert_json2html(self.object.metadata))  # nosec B308, B703
        else:
            context["metadata"] = None

        context["tabs"] = [
            {"title": artifact.plugin_name, "url": artifact.get_absolute_url()}
            for artifact in self.object.artifacts.all()
            if artifact.plugin_name not in HIDDEN_PLUGINS
        ]

        return context


class ArtifactDetailView(DetailView):
    """Artifact detail view."""

    template_name = "index/artifact_detail.html"
    slug_field = "plugin_name"

    def get_queryset(self) -> QuerySet:
        """Get the artifacts related to a link id."""
        link = get_object_or_404(Link, pk=self.kwargs["link_id"])
        return Artifact.objects.filter(link=link)

    def get_context_data(self, **kwargs) -> dict:
        """Add additional context for the templates."""
        context = super().get_context_data(**kwargs)
        context["artifacts"] = {}
        for artifact in self.object.link.artifacts.all():
            context["artifacts"][artifact.plugin_name] = artifact
        if self.object.link.metadata:
            context["metadata"] = mark_safe(convert_json2html(self.object.link.metadata))  # nosec B308, B703
        else:
            context["metadata"] = None

        context["tabs"] = [
            {"title": artifact.plugin_name, "url": artifact.get_absolute_url()}
            for artifact in self.object.link.artifacts.all()
            if artifact.plugin_name not in HIDDEN_PLUGINS
        ]

        return context


@method_decorator(csrf_exempt, name="dispatch")
class AddView(UserPassesTestMixin, FormView):
    """Add a new link."""

    template_name = "add.html"
    form_class = AddLinkForm

    def get_initial(self) -> dict:
        """Prefill the AddLinkForm with the 'url' GET parameter."""
        if self.request.method == "GET":
            url = self.request.GET.get("url", None)
            if url:
                return {"url": url if "://" in url else f"https://{url}"}

        return super().get_initial()

    def test_func(self) -> bool:
        """The test the user must pass to be able to add a link."""
        return settings.PUBLIC_ADD_VIEW or self.request.user.is_authenticated

    def get_context_data(self, **kwargs) -> dict:
        """Add additional context data for the templates."""
        return {
            **super().get_context_data(**kwargs),
            "title": "Add URLs",
            # We can't just call request.build_absolute_uri in the template, because it would include query parameters
            "absolute_add_path": self.request.build_absolute_uri(self.request.path),
            "VERSION": __version__,
            "FOOTER_INFO": "",
            "stdout": "",
        }

    def form_valid(self, form: AddLinkForm) -> None:
        """The form is valid, so save the link."""
        url = form.cleaned_data["url"]
        info(f"Adding URL: {url} with archivers: {form.cleaned_data['archivers']}")
        # extractors = ",".join(form.cleaned_data["archive_methods"])
        # input_kwargs = {
        #     "urls": url,
        #     "tag": tag,
        #     "depth": depth,
        #     "parser": parser,
        #     "update_all": False,
        #     "out_dir": OUTPUT_DIR,
        # }
        # if extractors:
        #     input_kwargs.update({"extractors": extractors})
        # add_stdout = StringIO()
        # with redirect_stdout(add_stdout):
        #     add(**input_kwargs)
        #     print(add_stdout.getvalue())
        #
        # context = self.get_context_data()
        #
        # context.update({"stdout": ansi_to_html(add_stdout.getvalue().strip()), "form": AddLinkForm()})
        # return render(template_name=self.template_name, request=self.request, context=context)
