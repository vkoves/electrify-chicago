import pytest
import shutil, os, pathlib
import pandas as pd
import numpy as np

from src.data.scripts.utils import get_and_clean_csv
from src.data.scripts import clean_and_pare_down_data_all_years as clean, process_data as proc
# from test.data.scripts.unit import save_test_file

src_dir = 'src'
test_dir = 'tests'
src_input_file = 'ChicagoEnergyBenchmarking.csv'
test_input_file = 'test_src_data.csv'
test_output_file = 'test_output.csv'

def get_file_path(dir: str, f: str):
    curr_path = pathlib.Path(".")
    path = curr_path.parent.absolute() / dir / "data" / "source"
    return os.path.join(path, f)

@pytest.fixture
def src_building_data() -> pd.DataFrame:
    test_data_path = get_file_path(test_dir, test_input_file)
    assert os.path.exists(test_data_path)
    return get_and_clean_csv(test_data_path)

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

def test_data_has_positive_ghg_data(test_columns_are_renamed):
    df = clean.get_all_ghg_data(test_columns_are_renamed)
    assert df is not None
    assert np.all(df['GHGIntensity'] > 0)

def test_data_has_submitted_status(test_columns_are_renamed):
    df = clean.get_submitted_data(test_columns_are_renamed)
    assert np.all(df['ReportingStatus'].str.contains('Submitted'))

@pytest.fixture
def test_has_last_year_of_data(test_columns_are_renamed) -> pd.DataFrame:
    df = clean.get_last_year_data(test_columns_are_renamed)
    assert np.all(df['ID'].value_counts() == 1)
    return df

@pytest.fixture
def fixed_strings(test_has_last_year_of_data, test_columns_are_renamed):
    return clean.fix_str_cols(test_has_last_year_of_data, 
                              test_columns_are_renamed)

def test_str_values_remain_the_same_as_origin(fixed_strings, test_has_last_year_of_data):
    assert test_has_last_year_of_data[clean.string_cols].equals(fixed_strings[clean.string_cols])

def test_lat_lon_become_strings(fixed_strings):
    df = fixed_strings[['Latitude','Longitude']]
    assert np.all(df.dtypes == 'string')
    
def test_int_values_remain_the_same_as_origin(test_has_last_year_of_data):
    df = clean.fix_int_cols(test_has_last_year_of_data)
    assert np.all(df[clean.int_cols].dtypes == 'Int64')

def test_csv_is_produced(test_has_last_year_of_data):
    out_file = get_file_path(test_dir, test_output_file)
    clean.output_to_csv(test_has_last_year_of_data, out_file)
    assert os.path.exists(out_file)

@pytest.fixture
def process():
    return clean.process(get_file_path(src_dir, src_input_file))

def test_data_has_ranking_columns(process):
    for col in proc.building_cols_to_rank:
        assert col in process.columns
