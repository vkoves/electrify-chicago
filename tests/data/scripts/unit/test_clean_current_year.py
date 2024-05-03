import pytest
import os
import csv
import pandas as pd

from src.data.scripts import clean_and_pare_down_data_current_year
from tests.data.scripts.utils import get_test_file_path

src_dir = 'src'
test_dir = 'tests'
test_input_file = 'test_src_data.csv'


@pytest.fixture
def csv_reader() -> csv.reader:
    '''return a csv.DictReader of our test data CSV'''

    csv_path = get_test_file_path(test_input_file)
    with open(csv_path) as filehandle:
        # yield here so that the context manager (with...)
        # can cleanup the open filehandle after we're done with
        # the csv.DictReader
        yield csv.DictReader(filehandle)


@pytest.fixture
def processed_dataframe() -> pd.DataFrame:
    '''Process our test data as per clean_and_pare_down_data_current_year.py
    and return the resulting dataframe'''

    input_filename = get_test_file_path(test_input_file)
    df = clean_and_pare_down_data_current_year.process(input_filename)
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


def test_lat_long_are_unchanged(processed_dataframe, csv_reader):
    '''confirm lat/long in the processed dataframe is unchanged from origin csv'''

    df = processed_dataframe
    df_lattitudes = [x for x in df['Latitude']]
    df_longitudes = [x for x in df['Longitude']]
    df_property_ids = [x for x in df['ID']]

    for row in csv_reader:
        csv_property_id = row['ID']
        csv_lat = row['Latitude']
        csv_long = row['Longitude']
        if csv_property_id in df_property_ids:
            i = df_property_ids.index(csv_property_id)
            assert (csv_lat, csv_long) == (df_lattitudes[i], df_longitudes[i])


def test_one_entry_per_property(processed_dataframe):
    '''confirm each property only has 1 entry in the processed dataframe'''

    df = processed_dataframe
    assert all([count == 1 for count in df['ID'].value_counts()])


def test_expected_columns_present(processed_dataframe):
    '''confirm all expected columns are present in the processed dataframe'''

    df = processed_dataframe
    mandatory_columns = (
        'DataYear',
        'ID',
        'PropertyName',
        'ReportingStatus',
        'Address',
        'ZIPCode',
        'ChicagoEnergyRating',
        'ExemptFromChicagoEnergyRating',
        'CommunityArea',
        'PrimaryPropertyType',
        'GrossFloorArea',
        'TotalGHGEmissions',
        'GHGIntensity',
        'YearBuilt',
        'NumberOfBuildings',
        'WaterUse',
        'ENERGYSTARScore',
        'ElectricityUse',
        'NaturalGasUse',
        'DistrictSteamUse',
        'DistrictChilledWaterUse',
        'AllOtherFuelUse',
        'SiteEUI',
        'SourceEUI',
        'WeatherNormalizedSiteEUI',
        'WeatherNormalizedSourceEUI',
        'Latitude',
        'Longitude',
        'Location',
        'Row_ID',
        'Wards',
        'CommunityAreas',
        'ZipCodes',
        'CensusTracts',
        'HistoricalWards2003-2015',
    )
    assert set(df.columns) == set(mandatory_columns)


def test_correct_year_selected(processed_dataframe):
    '''confirm the correct DataYear is present in the processed dataframe'''

    df = processed_dataframe

    non_2022_df = df[~df['DataYear']==2022]
    assert len(non_2022_df) == 0

    yr_2022_df = df[df['DataYear']==2022]
    assert len(yr_2022_df) == 2


def test_property_count(processed_dataframe):
    '''confirm the processed dataframe has the correct number of properties'''

    df = processed_dataframe
    assert len(df) == 2


def test_no_ghg_property_is_excluded(processed_dataframe):
    '''confirm property with submitted data but no GHGIntensity data
    ie excluded from the processed dataframe'''

    df = processed_dataframe
    # property ID 240068 is present in test source data but
    # 2016-2022 submitted data has no GHGIntensity data
    assert len(df[df['ID']=='240068']) == 0
