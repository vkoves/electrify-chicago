import pytest
import shutil, os, pathlib
import pandas as pd
import numpy as np

from src.data.scripts.utils import get_and_clean_csv
from src.data.scripts import clean_and_pare_down_data_all_years as clean

file_to_copy = "ChicagoEnergyBenchmarking.csv"

def get_file_path(dir: str, f: str):
    curr_path = pathlib.Path(".")
    path = curr_path.parent.absolute() / dir / "data" / "source"
    return os.path.join(path, f)

@pytest.fixture
def get_src_file_path():
    return get_file_path("src", file_to_copy)

@pytest.fixture
def get_test_file_path():
    return get_file_path("test", file_to_copy)

@pytest.fixture
def copy_file(get_src_file_path, get_test_file_path):
    if not os.path.exists(get_test_file_path):
        print(os.path.dirname(get_src_file_path))
        os.makedirs(os.path.dirname(get_test_file_path), exist_ok=True)
        shutil.copy(get_src_file_path, get_test_file_path)
        assert pathlib.Path(get_test_file_path).exists()
    return get_test_file_path

@pytest.fixture
def src_building_data(copy_file):
    # currently equivalent to
    # return pd.read_csv(copy_file)
    return get_and_clean_csv(copy_file)

@pytest.mark.parametrize("test_input", [
    clean.string_cols,
    clean.int_cols,
    clean.replace_headers
])
def test_is_not_empty(test_input):
    assert len(test_input) > 0

def test_src_data_exists(src_building_data):
    assert src_building_data is not None

@pytest.fixture
def test_columns_are_renamed(src_building_data):
    df = clean.rename_columns(src_building_data)
    assert df is not None
    assert not df.columns.equals(src_building_data.columns)
    return df

def test_nonzero_ghg_filter(test_columns_are_renamed):
    df = clean.get_all_ghg_data(test_columns_are_renamed)
    assert df is not None
    assert np.all(df['GHGIntensity'] > 0)

def test_filter_submitted_data(test_columns_are_renamed):
    df = clean.get_submitted_data(test_columns_are_renamed)
    assert np.all(df['ReportingStatus'].str.contains('Submitted'))

def test_main():
    pass
