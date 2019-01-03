# encoding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import collections
import logging
import re

import six

logger = logging.getLogger(__name__)


class RowWrapper(object):
    """
    Build lightweight row tuples for DB API and csv.DictReader rows.

    Inspired by Greg Stein's lovely dtuple module,
    https://code.activestate.com/recipes/81252-using-dtuple-for-flexible-query-result-access,
    which I can't find online any longer, isn't on pypi, and doesn't support Python 3 without some fixes.

    Initializer takes a sequence of column descriptions, either names, or tuples of names and other metadata (which
    will be ignored). For instance, it's happy to take a DB API cursor description, or a csv.DictReader's fieldnames
    property. Provides a wrap(row) method for wrapping rows.

    Some characters which are illegal in identifiers will be replaced when building the row tuples - currently "-" and
    " " characters will be replaced with "_"s.

    >>> cursor = conn.cursor()
    >>> cursor.execute("SELECT kind, rating FROM sausages ORDER BY rating DESC;")
    >>> wrapper = RowWrapper(cursor.description)
    >>> rows = [wrapper.wrap(row) for row in cursor.fetchall()]

    >>> reader = csv.DictReader(csv_file)
    >>> wrapper = RowWrapper(reader.fieldnames)
    >>> rows = [wrapper.wrap(row) for row in reader]
    """

    def __init__(self, description, force_lower_case_ids=False):
        column_names = (
            [col for col in description]
            if isinstance(description[0], six.string_types)
            else [col[0] for col in description]
        )
        self.ids_and_column_names = self._ids_and_column_names(column_names, force_lower_case=force_lower_case_ids)
        self.namedtuple = collections.namedtuple("RowTuple", self.ids_and_column_names.keys())

    @staticmethod
    def _ids_and_column_names(names, force_lower_case=False):
        """Ensure all column names are unique identifiers."""
        fixed = collections.OrderedDict()
        for name in names:
            identifier = RowWrapper._make_identifier(name)
            if force_lower_case:
                identifier = identifier.lower()
            while identifier in fixed:
                identifier = RowWrapper._increment_numeric_suffix(identifier)
            fixed[identifier] = name
        return fixed

    @staticmethod
    def _make_identifier(string):
        """Attempt to convert string into a valid identifier by replacing invalid characters with "_"s,
        and prefixing with "a_" if necessary."""
        string = re.sub(r"[ \-+/\\*%&$£#@.,;:'" "?<>]", "_", string)
        if re.match(r"^\d", string):
            string = "a_{0}".format(string)
        return string

    @staticmethod
    def _increment_numeric_suffix(s):
        """Increment (or add) numeric suffix to identifier."""
        if re.match(r".*\d+$", s):
            return re.sub(r"\d+$", lambda n: str(int(n.group(0)) + 1), s)
        return s + "_2"

    def wrap(self, row):
        """Return row tuple for row."""
        return (
            self.namedtuple(**{ident: row[column_name] for ident, column_name in self.ids_and_column_names.items()})
            if isinstance(row, collections.Mapping)
            else self.namedtuple(**{ident: val for ident, val in zip(self.ids_and_column_names.keys(), row)})
        )

    def wrap_all(self, rows):
        """Return row tuple for each row in rows."""
        return (self.wrap(r) for r in rows)

    def __call__(self, row):
        return self.wrap(row)
