import pytest

from src.data.scripts import clean_and_pare_down_data_all_years

def test_string_cols_is_not_empty():
    assert len(clean_and_pare_down_data_all_years.string_cols) > 0

def test_int_cols_is_not_empty():
    assert len(clean_and_pare_down_data_all_years.int_cols) > 0

def test_replacement_headers_is_not_empty():
    assert len(clean_and_pare_down_data_all_years.replace_headers) > 0