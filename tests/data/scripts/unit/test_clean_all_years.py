import pytest
import shutil, os, pathlib
import pandas as pd
import numpy as np

from src.data.scripts.utils import get_and_clean_csv
from src.data.scripts import clean_and_pare_down_data_all_years as clean
# from test.data.scripts.unit import save_test_file

property_test_cases = ['United Center']
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
def src_data():
    file_path = get_file_path(src_dir, src_input_file)
    return get_and_clean_csv(file_path)

@pytest.fixture
def test_data_has_relevant_sample(src_data):
    # check that all test cases exist at least once in data set
    assert len(src_data) > 0
    contains_test_cases = []
    for p in property_test_cases:
        has_related_name = src_data['Property Name'].map(lambda x: True if p in str(x) else False)
        contains_test_cases.append(np.any(has_related_name))
    assert np.all(contains_test_cases)
    test_cases = src_data['Property Name'].str.contains('|'.join(property_test_cases), na=False)
    return src_data[test_cases]

@pytest.fixture
def save_test_src(test_data_has_relevant_sample):
    file_path = get_file_path(test_dir, test_input_file)
    assert len(test_data_has_relevant_sample) > 0
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        test_data_has_relevant_sample.to_csv(file_path, index=False)
    return file_path

@pytest.fixture
def src_building_data(save_test_src) -> pd.DataFrame:
    assert os.path.exists(save_test_src)
    return get_and_clean_csv(save_test_src)

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
    out_file = get_file_path(test_dir, test_output_file)
    clean.output_to_csv(test_has_last_year_of_data, out_file)
    assert os.path.exists(out_file)
