"""Test tag models."""

import pytest

from ..factories import LinkFactory, TagFactory

pytestmark = pytest.mark.django_db


def test_tag_substitute_replaces():
    """Substituting a tag should change the links."""
    tag1 = TagFactory()
    tag2 = TagFactory()
    link1 = LinkFactory()
    link1.tags.add(tag1)
    assert tag1.links.all()[0] == link1

    tag1.substitute = tag2
    tag1.save()
    assert tag1.links.all().count() == 0
    assert tag2.links.all().count() == 1
    assert tag2.links.all()[0] == link1


def test_tag_substitute_subs():
    """Assigning a link to a substituted tag should tag the substitute."""
    tag2 = TagFactory()
    tag1 = TagFactory(substitute=tag2)
    link1 = LinkFactory()
    link1.tags.add(tag1)
    assert tag1.links.all().count() == 0
    assert tag2.links.all().count() == 1
    assert tag2.links.all()[0] == link1


def test_tag_disabled_tag_removes_links():
    """Disabling a tag removes the links to it."""
    tag1 = TagFactory()
    link1 = LinkFactory()
    link1.tags.add(tag1)
    assert tag1.links.all().count() == 1
    tag1.enabled = False
    tag1.save()
    assert tag1.links.all().count() == 0


def test_tag_disabled_tag_cant_be_used():
    """You can't assign a link to a disabled tag."""
    tag1 = TagFactory(enabled=False)
    link1 = LinkFactory()
    link1.tags.add(tag1)
    assert tag1.links.all().count() == 0


def test_tag_attributes():
    """Test the basic attributes of a tag."""
    tag1 = TagFactory(name="foo bar")
    assert tag1.name == "foo bar"
    assert tag1.slug == "foo-bar"
    assert f"{tag1}" == "foo bar"
    assert tag1.enabled is True
    assert tag1.substitute is None
