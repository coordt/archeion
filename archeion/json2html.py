"""
JSON 2 HTML Converter.

(c) Varun Malhotra 2013-2021
Source Code: https://github.com/softvar/json2html


Contributors:
-------------
1. Michel Müller (@muellermichel), https://github.com/softvar/json2html/pull/2
2. Daniel Lekic (@lekic), https://github.com/softvar/json2html/pull/17
3. Corey Oordt (@coordt), here.

LICENSE: MIT
--------
"""
import json as json_parser
from collections import OrderedDict
from html import escape as html_escape
from string import Template
from typing import Any, Callable, Dict, List, Optional

TABLE_WRAPPER = "<table>\n<tbody>\n${rows}\n</tbody>\n</table>"
ROW_WRAPPER = "<tr>\n<th>${key}</th>\n<td>${value}</td></tr>"
LIST_WRAPPER = "<ul>\n${items}\n</ul>"
LIST_ITEM_WRAPPER = "<li>${item}</li>"

DICT_TYPES = (dict, OrderedDict)
ITERABLE_TYPES = (list, set, tuple)


class TableWrapper:
    """Wrap a set of rows in a table."""

    def __init__(self, table_template: str = TABLE_WRAPPER, row_template: str = ROW_WRAPPER):
        self.table_template = Template(table_template)
        self.row_template = Template(row_template)

    def render_rows(self, rows: List[Dict[str, Any]]) -> str:
        """Render a list of rows as a table."""
        return "\n".join([self.row_template.safe_substitute(**item) for item in rows])

    def __call__(self, rows: List[Dict[str, str]]):
        """Render the table."""
        return self.table_template.substitute(rows=self.render_rows(rows))


TableWrapperType = Callable[[List[Dict[str, str]]], str]


class ListWrapper:
    """Wrap a list of values into a list."""

    def __init__(self, list_template: str = LIST_WRAPPER, list_item_template: str = LIST_ITEM_WRAPPER):
        self.list_template = Template(list_template)
        self.list_item_template = Template(list_item_template)

    def render_items(self, items: List[Any]) -> str:
        """Render all the items."""
        return "\n".join([self.list_item_template.safe_substitute(item=item) for item in items])

    def __call__(self, items: List[Any]) -> str:
        """Render the list."""
        return self.list_template.substitute(items=self.render_items(items))


ListWrapperType = Callable[[List[Any]], str]


def convert_json2html(
    value: Any, table_wrapper: Optional[TableWrapperType] = None, list_wrapper: Optional[ListWrapperType] = None
) -> str:
    """
    Convert JSON to HTML Table format.
    """
    if not value:
        json_input = {}
    elif isinstance(value, str):
        json_input = json_parser.loads(value)
    else:
        json_input = value

    table_wrapper = table_wrapper or TableWrapper()
    list_wrapper = list_wrapper or ListWrapper()

    return convert_json_node(json_input, table_wrapper, list_wrapper)


def convert_json_node(json_input: Any, table_wrapper: TableWrapperType, list_wrapper: ListWrapperType) -> str:
    """
    Dispatch JSON input according to the outermost type and process it to generate the super awesome HTML format.
    """
    if isinstance(json_input, DICT_TYPES):
        rows = [
            {
                "key": convert_json_node(key, table_wrapper, list_wrapper),
                "value": convert_json_node(val, table_wrapper, list_wrapper),
            }
            for key, val in json_input.items()
        ]
        return table_wrapper(rows)
    if isinstance(json_input, ITERABLE_TYPES):
        items = [convert_json_node(item, table_wrapper, list_wrapper) for item in json_input]
        return list_wrapper(items)
    return html_escape(str(json_input))
