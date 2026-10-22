# Copyright 2018-2026 Simon Brunning
import csv
import logging
from collections.abc import Iterable
from sqlite3 import Connection

from hamcrest import assert_that, contains_exactly, has_properties

from brunns.row.rowwrapper import RowWrapper

logger = logging.getLogger(__name__)


def test_dbapi_row_wrapping(db: Connection):
    # Given
    cursor = db.cursor()
    cursor.execute("SELECT kind, rating FROM sausages ORDER BY rating DESC;")

    # When
    wrapper = RowWrapper(cursor.description)
    rows = [wrapper.wrap(row) for row in cursor.fetchall()]

    # Then
    assert_that(
        rows,
        contains_exactly(
            has_properties(kind="cumberland", rating=10),
            has_properties(kind="lincolnshire", rating=9),
            has_properties(kind="vegetarian", rating=0),
        ),
    )


def test_wrap_all(db: Connection):
    # Given
    cursor = db.cursor()
    cursor.execute("SELECT kind, rating FROM sausages ORDER BY rating DESC;")

    # When
    wrapper = RowWrapper(cursor.description)
    rows = wrapper.wrap_all(cursor.fetchall())

    # Then
    assert_that(
        rows,
        contains_exactly(
            has_properties(kind="cumberland", rating=10),
            has_properties(kind="lincolnshire", rating=9),
            has_properties(kind="vegetarian", rating=0),
        ),
    )


def test_csv_wrapping(csv_file: Iterable[str]):
    # Given
    reader = csv.DictReader(csv_file)

    # When
    wrapper = RowWrapper(reader.fieldnames)
    rows = [wrapper.wrap(row) for row in reader]

    # Then
    assert_that(
        rows,
        contains_exactly(
            has_properties(kind="cumberland", rating="10"),
            has_properties(kind="lincolnshire", rating="9"),
            has_properties(kind="vegetarian", rating="0"),
        ),
    )
