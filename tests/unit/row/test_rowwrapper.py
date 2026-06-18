import logging
from dataclasses import FrozenInstanceError

import pytest
from brunns.matchers.object import has_repr
from hamcrest import assert_that, has_properties

from brunns.row.rowwrapper import RowWrapper

logger = logging.getLogger(__name__)


def test_identifiers_fixed_for_mapping_row():
    # Given
    wrapper = RowWrapper(["column-name", "Another One", "3rd Column"])

    # When
    row = wrapper({"column-name": "value", "Another One": "another-value", "3rd Column": "3rd value"})

    # Then
    assert_that(
        row,
        has_properties(column_name="value", Another_One="another-value", a_3rd_Column="3rd value"),
    )


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
    assert_that(
        row,
        has_properties(column_name="value", column_name_2="another", column_name_3="yet another"),
    )


def test_curly_brace_identifiers_for_mapping_row():
    # Given
    wrapper = RowWrapper(["{Ix}", "{Ex}", "{Cx}"])

    # When
    row = wrapper({"{Ix}": "1", "{Ex}": "2", "{Cx}": "3"})

    # Then
    assert_that(row, has_properties(_Ix_="1", _Ex_="2", _Cx_="3"))


def test_lower_cased_identifiers():
    # Given
    wrapper = RowWrapper(["column-name", "Another One", "3rd Column"], force_lower_case_ids=True)

    # When
    row = wrapper({"column-name": "value", "Another One": "another-value", "3rd Column": "3rd value"})

    # Then
    assert_that(
        row,
        has_properties(column_name="value", another_one="another-value", a_3rd_column="3rd value"),
    )


def test_immutable_by_default():
    # Given
    wrapper = RowWrapper(["column-1", "column-2"])

    # When
    row = wrapper(["value 1", "value 2"])

    # Then
    with pytest.raises(FrozenInstanceError):
        row.column_1 = "new value"


def test_mutability():
    # Given
    wrapper = RowWrapper(["column-1", "column-2"], mutable=True)

    # When
    row = wrapper(["value 1", "value 2"])

    # Then
    row.column_1 = "new value"


def test_unordered_by_default():
    # Given
    wrapper = RowWrapper(["column-1", "column-2"])

    # When
    rows = list(wrapper.wrap_all([["value 1", "value 2"], ["value 3", "value 4"]]))

    # Then
    with pytest.raises(TypeError):
        rows.sort()


def test_ordered():
    # Given
    wrapper = RowWrapper(["column-1", "column-2"], ordered=True)

    # When
    rows = list(wrapper.wrap_all([["value 1", "value 2"], ["value 3", "value 4"]]))

    # Then
    rows.sort()


def test_hashable():
    # Given
    wrapper = RowWrapper(["column-1", "column-2"])

    # When
    row = wrapper(["value 1", "value 2"])

    # Then
    hash(row)


def test_repr():
    # Given
    wrapper = RowWrapper(["kind", "rating"], row_tuple_class_name="Sausage")

    # When
    row = wrapper(["Cumberland", 10])

    # Then
    assert_that(row, has_repr("Sausage(kind='Cumberland', rating=10)"))
