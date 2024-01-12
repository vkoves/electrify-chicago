import pytest

from src.data.scripts import clean_and_pare_down_data_current_year as clean

def test_string_cols_is_not_empty():
    assert len(clean.string_cols) > 0

def test_int_cols_is_not_empty():
    assert len(clean.int_cols) > 0