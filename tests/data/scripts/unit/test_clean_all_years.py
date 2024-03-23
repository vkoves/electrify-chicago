import pytest
import shutil, os, pathlib, csv
import pandas as pd
import numpy as np

from src.data.scripts.utils import get_and_clean_csv
from src.data.scripts import clean_and_pare_down_data_all_years as clean, process_data as proc
from tests.data.scripts.utils import get_test_file_path, get_src_file_path

src_dir = 'src'
test_dir = 'tests'
src_input_file = 'ChicagoEnergyBenchmarking.csv'
test_input_file = 'test_src_data.csv'
test_output_file = 'test_output.csv'

@pytest.fixture
def src_building_data() -> pd.DataFrame:
    test_data_path = get_test_file_path(test_input_file)
    assert os.path.exists(test_data_path)
    return get_and_clean_csv(test_data_path)

@pytest.fixture
def csv_file() -> csv.reader:
    csvfile = open(get_test_file_path(test_input_file))
    return csv.reader(csvfile)

def test_csv_file_has_some_data(csv_file):
    first_line = csv_file.__next__()
    assert first_line
    assert len(first_line) > 0

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
    df = clean.get_buildings_with_ghg_intensity(test_columns_are_renamed)
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

@pytest.fixture
def fixed_strings_all_years(test_columns_are_renamed):
    return clean.fix_str_cols(test_columns_are_renamed,
                              test_columns_are_renamed)

def test_str_values_remain_the_same_as_origin(fixed_strings_all_years, csv_file):
    header_row = next(csv_file)
    str_col_positions = list(map(lambda col: fixed_strings_all_years.columns.get_loc(col), clean.string_cols))
    for csv_row in csv_file:
        year, id = csv_row[0], csv_row[1]
        row = fixed_strings_all_years[(fixed_strings_all_years['ID'].astype(str) == id) & \
                                      (fixed_strings_all_years['DataYear'].astype(str) == year)]

        for col, csv_pos in zip(clean.string_cols, str_col_positions):
            if all(pd.isna(row[col].to_numpy())):
                continue

            # The raw GPS in ChicagoEnergyBenchmarking.csv has 41.880451999999998, which gets
            # truncated, so we round to ignore that, since it's not a significant difference
            # TODO: Fix GPS inconsistency and drop  rounding
            csv_value = csv_row[csv_pos]


            # If > 10 or < -10, we truncate 0 after rounding to 6 decimals. This means this applies
            # to GPS coordinates but not energy star ratings (e.g.)
            if (abs(float(csv_value)) > 10):
                print("df ", row[col].to_numpy(), "csv ", csv_value)
                csv_float = float(csv_value)
                csv_val_parsed = f'{csv_float:.9f}'.rstrip('0').rstrip('.')
            else:
                csv_val_parsed = csv_value

            assert row[col].to_numpy()[0] == csv_val_parsed

def test_lat_lon_become_strings(fixed_strings):
    df = fixed_strings[['Latitude','Longitude']]
    assert np.all(df.dtypes == 'string')

def test_int_values_remain_the_same_as_origin(test_has_last_year_of_data):
    df = clean.fix_int_cols(test_has_last_year_of_data)
    assert np.all(df[clean.int_cols].dtypes == 'Int64')

def test_csv_is_produced(test_has_last_year_of_data):
    out_file = get_test_file_path(test_output_file)
    clean.output_to_csv(test_has_last_year_of_data, out_file)
    assert os.path.exists(out_file)

@pytest.fixture
def process():
    return clean.process(get_src_file_path(src_input_file))

def test_data_has_ranking_columns(process):
    for col in proc.building_cols_to_rank:
        assert col in process.columns
