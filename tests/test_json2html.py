"""Test json2html.py."""

import pytest
from pytest import param

from archeion import json2html

TWRAP = json2html.TableWrapper(table_template="<t>${rows}</t>", row_template="<r>${key}|${value}</r>")
LWRAP = json2html.ListWrapper(list_template="<l>${items}</l>", list_item_template="<i>${item}</i>")


@pytest.mark.parametrize(
    "value, expected",
    [
        param(
            {"string_key": "string_value"},
            "<t><r>string_key|string_value</r></t>",
            id="dict-string-value",
        ),
        param(
            {"string_key": 24},
            "<t><r>string_key|24</r></t>",
            id="dict-int-value",
        ),
        param(
            {"string_key": 3.14},
            "<t><r>string_key|3.14</r></t>",
            id="dict-float-value",
        ),
        param(
            {"string_key": True},
            "<t><r>string_key|True</r></t>",
            id="dict-bool-value",
        ),
        param(
            {"string_key": None},
            "<t><r>string_key|None</r></t>",
            id="dict-none-value",
        ),
        param(
            {"string_key": [1, "2", 3.14]},
            "<t><r>string_key|<l><i>1</i>\n<i>2</i>\n<i>3.14</i></l></r></t>",
            id="dict-list-value",
        ),
        param(
            [1, "2", 3.14],
            "<l><i>1</i>\n<i>2</i>\n<i>3.14</i></l>",
            id="list",
        ),
        param(
            "string value",
            "string value",
            id="string-value",
        ),
    ],
)
def test_convert_object(value, expected):
    assert json2html.convert_json_node(value, table_wrapper=TWRAP, list_wrapper=LWRAP) == expected


def test_convert():
    assert (
        json2html.convert_json2html('{"string_key": "string_value"}', table_wrapper=TWRAP, list_wrapper=LWRAP)
        == "<t><r>string_key|string_value</r></t>"
    )
