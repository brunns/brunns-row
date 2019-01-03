# encoding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from hamcrest import assert_that, has_properties

from brunns.row.rowwrapper import RowWrapper

logger = logging.getLogger(__name__)


def test_identifiers_fixed_for_mapping_row():
    # Given
    wrapper = RowWrapper(["column-name", "Another One", "3rd Column"])

    # When
    row = wrapper({"column-name": "value", "Another One": "another-value", "3rd Column": "3rd value"})

    # Then
    assert_that(row, has_properties(column_name="value", Another_One="another-value", a_3rd_Column="3rd value"))


def test_identifiers_fixed_for_positional_row():
    # Given
    wrapper = RowWrapper(["column-name", "Another One", "3rd Column"])

    # When
    row = wrapper(["value", "another", "yet another"])

    # Then
    assert_that(row, has_properties(column_name="value", Another_One="another", a_3rd_Column="yet another"))


def test_column_identifiers_deduplication_for_mapping_row():
    # Given
    wrapper = RowWrapper(["column-name", "column$name"])

    # When
    row = wrapper({"column-name": "value", "column$name": "another-value"})

    # Then
    assert_that(row, has_properties(column_name="value", column_name_2="another-value"))


def test_column_identifiers_deduplication_for_positional_row():
    # Given
    wrapper = RowWrapper(["column-name", "column-name", "column$name"])

    # When
    row = wrapper(["value", "another", "yet another"])

    # Then
    assert_that(row, has_properties(column_name="value", column_name_2="another", column_name_3="yet another"))


def test_lower_cased_identifiers():
    # Given
    wrapper = RowWrapper(["column-name", "Another One", "3rd Column"], force_lower_case_ids=True)

    # When
    row = wrapper({"column-name": "value", "Another One": "another-value", "3rd Column": "3rd value"})

    # Then
    assert_that(row, has_properties(column_name="value", another_one="another-value", a_3rd_column="3rd value"))
