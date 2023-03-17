"""Creates fake data for testing."""

import factory
from factory import Faker
from factory.django import DjangoModelFactory

from archeion.archivers import get_archivers_map
from archeion.index.models import Artifact, ArtifactStatus, Link, Tag


class TagFactory(DjangoModelFactory):

    name = Faker("word")
    enabled = True
    substitute = None

    class Meta:
        model = Tag
        django_get_or_create = ["name"]


class LinkFactory(DjangoModelFactory):
    url = Faker("uri")
    content_type = "text/html"

    class Meta:
        model = Link
        django_get_or_create = ["url"]


class ArtifactFactory(DjangoModelFactory):
    link = factory.SubFactory(LinkFactory)
    plugin_name = Faker("word", ext_word_list=get_archivers_map().keys())
    output_path = Faker("file_path", absolute=False)
    status = Faker("enum", enum_cls=ArtifactStatus)

    class Meta:
        model = Artifact
        django_get_or_create = ["link", "plugin_name"]
