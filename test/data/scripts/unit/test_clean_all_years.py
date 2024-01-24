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
def src_building_data(copy_file) -> pd.DataFrame:
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
def test_columns_are_renamed(src_building_data) -> pd.DataFrame:
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

@pytest.fixture
def test_has_last_year_of_data(test_columns_are_renamed) -> pd.DataFrame:
    df = clean.get_last_year_data(test_columns_are_renamed)
    assert np.all(df['ID'].value_counts() == 1)
    return df

def test_str_values_remain_the_same(test_has_last_year_of_data, test_columns_are_renamed):
    df = clean.fix_str_cols(test_has_last_year_of_data, test_columns_are_renamed)
    assert test_has_last_year_of_data[clean.string_cols].equals(df[clean.string_cols])
    
def test_int_values_remain_the_same(test_has_last_year_of_data):
    df = clean.fix_int_cols(test_has_last_year_of_data)
    assert np.all(df[clean.int_cols].dtypes == 'Int64')

def test_output_produces_csv(test_has_last_year_of_data):
    out_file = get_file_path("test", "test_output.csv")
    clean.output_to_csv(test_has_last_year_of_data, out_file)
    assert os.path.exists(out_file)
