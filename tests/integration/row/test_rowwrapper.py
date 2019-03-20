# encoding=utf-8
import csv
import logging

from brunns.row.rowwrapper import RowWrapper
from hamcrest import assert_that
from hamcrest import contains
from hamcrest import has_properties

logger = logging.getLogger(__name__)


def test_dbapi_row_wrapping(db):
    # Given
    cursor = db.cursor()
    cursor.execute("SELECT kind, rating FROM sausages ORDER BY rating DESC;")

    # When
    wrapper = RowWrapper(cursor.description)
    rows = [wrapper.wrap(row) for row in cursor.fetchall()]

    # Then
    assert_that(
        rows,
        contains(
            has_properties(kind="cumberland", rating=10),
            has_properties(kind="lincolnshire", rating=9),
            has_properties(kind="vegetarian", rating=0),
        ),
    )


def test_wrap_all(db):
    # Given
    cursor = db.cursor()
    cursor.execute("SELECT kind, rating FROM sausages ORDER BY rating DESC;")

    # When
    wrapper = RowWrapper(cursor.description)
    rows = wrapper.wrap_all(cursor.fetchall())

    # Then
    assert_that(
        rows,
        contains(
            has_properties(kind="cumberland", rating=10),
            has_properties(kind="lincolnshire", rating=9),
            has_properties(kind="vegetarian", rating=0),
        ),
    )


def test_csv_wrapping(csv_file):
    # Given
    reader = csv.DictReader(csv_file)

    # When
    wrapper = RowWrapper(reader.fieldnames)
    rows = [wrapper.wrap(row) for row in reader]

    # Then
    assert_that(
        rows,
        contains(
            has_properties(kind="cumberland", rating="10"),
            has_properties(kind="lincolnshire", rating="9"),
            has_properties(kind="vegetarian", rating="0"),
        ),
    )
