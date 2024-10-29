import pandas as pd
import pytest

from src.data.scripts import clean_and_pare_down_data_all_years
from tests.data.scripts.utils import get_test_file_path

src_dir = 'src'
test_dir = 'tests'
test_input_file = 'test_src_data.csv'
test_output_file = 'test_output.csv'


@pytest.fixture
def processed_dataframe() -> pd.DataFrame:
    '''Process our test data as per clean_and_pare_down_data_all_years.py
    and return the resulting dataframe'''

    input_filename = get_test_file_path(test_input_file)
    df = clean_and_pare_down_data_all_years.process(input_filename, False)
    assert df is not None
    return df

def test_data_has_positive_ghg_data(processed_dataframe):
    '''confirm each property in the processed dataframe has non-zero GHGIntensity'''

    df = processed_dataframe
    assert all([ghg > 0 for ghg in df['GHGIntensity']])


def test_data_has_submitted_status(processed_dataframe):
    '''confirm each property in the processed dataframe has a submitted status'''

    df = processed_dataframe
    for status in df['ReportingStatus']:
        assert status in ('Submitted Data', 'Submitted')


def test_expected_columns_present(processed_dataframe):
    '''confirm all expected columns are present in the processed dataframe'''

    df = processed_dataframe
    mandatory_columns = clean_and_pare_down_data_all_years.columns_to_track_over_time
    assert set(df.columns) == set(mandatory_columns)


def test_record_count_per_building(processed_dataframe):
    '''confirm the correct number of records is present in the processed
    dataframe for a sample of properties'''

    df = processed_dataframe

    united_center_df = df[df['ID']==100856]
    assert len(united_center_df) == 5

    crown_hall_df = df[df['ID']==256419]
    assert len(crown_hall_df) == 3

    bldg_138730_df = df[df['ID']==138730]
    assert len(bldg_138730_df) == 3


def test_total_record_count(processed_dataframe):
    '''confirm the processed dataframe has the correct number of records'''

    df = processed_dataframe
    assert len(df) == 26


def test_no_ghg_property_is_excluded(processed_dataframe):
    '''confirm property with submitted data but no GHGIntensity data
    ie excluded from the processed dataframe'''

    df = processed_dataframe
    # property ID 240068 is present in test source data but
    # 2016-2022 submitted data has no GHGIntensity data
    assert len(df[df['ID']=='240068']) == 0
