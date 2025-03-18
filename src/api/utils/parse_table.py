__all__ = ["parse_table"]

from bs4 import Tag

from .exceptions import AnimeFLVParseError


def parse_table(table: Tag):
    columns = list([x.string for x in table.thead.tr.find_all("th")])
    rows = []

    for row in table.tbody.find_all("tr"):
        values = row.find_all("td")

        if len(values) != len(columns):
            raise AnimeFLVParseError("Don't match values size with columns size")

        rows.append({h: x for h, x in zip(columns, values)})

    return rows
