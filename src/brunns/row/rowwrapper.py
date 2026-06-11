import dataclasses
import logging
import re
from collections import OrderedDict
from collections.abc import Iterable, Iterator, Mapping, Sequence
from typing import Any

logger = logging.getLogger(__name__)


class RowWrapper:
    """
    Build lightweight row tuples for DB API and csv.DictReader rows.

    Inspired by Greg Stein's lovely
    `dtuple module <https://code.activestate.com/recipes/81252-using-dtuple-for-flexible-query-result-access>`_,
    which I can't find online any longer, isn't on pypi, and doesn't support Python 3 without some fixes.

    Initializer takes a sequence of column descriptions, either names, or tuples of names and other metadata (which
    will be ignored). For instance, it's happy to take a DB API cursor description, or a csv.DictReader's fieldnames
    property. Provides a wrap(row) method for wrapping rows, and a wrap_all(rows) method for wrapping a collection
    of rows.

    Characters which are illegal in identifiers will be replaced when building the row tuples - any non-word character
    will be replaced with "_".

    >>> cursor = conn.cursor()
    >>> cursor.execute("SELECT kind, rating FROM sausages ORDER BY rating DESC;")
    >>> wrapper = RowWrapper(cursor.description)
    >>> rows = [wrapper.wrap(row) for row in cursor.fetchall()]

    >>> reader = csv.DictReader(csv_file)
    >>> wrapper = RowWrapper(reader.fieldnames)
    >>> rows = [wrapper.wrap(row) for row in reader]
    """

    def __init__(
        self,
        description: Sequence[
            str | tuple[str, ...]
        ],  # TODO: We can use "Sequence[str | tuple[str, *tuple[Any, ...]]]" once we drop Python 3.10 support.
        force_lower_case_ids: bool = False,
        row_tuple_class_name: str = "Row",
    ) -> None:
        column_names: list[str] = [col if isinstance(col, str) else col[0] for col in description]
        self.ids_and_column_names = self._ids_and_column_names(column_names, force_lower_case=force_lower_case_ids)
        self.dataclass = dataclasses.make_dataclass(row_tuple_class_name, self.ids_and_column_names.keys())

    @staticmethod
    def _ids_and_column_names(names: Sequence[str], force_lower_case: bool = False) -> OrderedDict[str, str]:
        """Ensure all column names are unique identifiers."""
        fixed = OrderedDict()
        for name in names:
            identifier = RowWrapper._make_identifier(name)
            if force_lower_case:
                identifier = identifier.lower()
            while identifier in fixed:
                identifier = RowWrapper._increment_numeric_suffix(identifier)
            fixed[identifier] = name
        return fixed

    @staticmethod
    def _make_identifier(string: str) -> str:
        """Attempt to convert string into a valid identifier by replacing invalid characters with "_"s,
        and prefixing with "a_" if necessary."""
        string = re.sub(r"\W", "_", string)
        if re.match(r"^\d", string):
            string = f"a_{string}"
        return string

    @staticmethod
    def _increment_numeric_suffix(s: str) -> str:
        """Increment (or add) numeric suffix to identifier."""
        if re.match(r".*\d+$", s):
            return re.sub(r"\d+$", lambda n: str(int(n.group(0)) + 1), s)
        return s + "_2"

    def wrap(self, row: Mapping[str, Any] | Sequence[Any]) -> Any:
        """Return row tuple for row."""
        return (
            self.dataclass(**{ident: row[column_name] for ident, column_name in self.ids_and_column_names.items()})
            if isinstance(row, Mapping)
            else self.dataclass(**dict(zip(self.ids_and_column_names.keys(), row, strict=False)))
        )

    def wrap_all(self, rows: Iterable[Mapping[str, Any] | Sequence[Any]]) -> Iterator[Any]:
        """Return row tuple for each row in rows."""
        return (self.wrap(r) for r in rows)

    def __call__(self, row: Mapping[str, Any] | Sequence[Any]) -> Any:
        return self.wrap(row)
