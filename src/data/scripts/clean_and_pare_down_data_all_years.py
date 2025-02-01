"""
The initial processing file for the Electrify Chicago Data pipeline

Ingests the initial city data CSV and renames its column headers for GraphQL compatibility in
Gridsome, and outputs two files into the dist/ directory, one with a limited number of columns
across all years (our historic data) and one with all columns for the latest year.

This is done because we only show historic data on individual building pages, and loading the
historic data on pages like search and the homepage would get quite heavy.
"""

import pandas as pd
from src.data.scripts.utils import get_and_clean_csv, get_data_file_path

file_dir = 'source'
out_file_dir = 'dist'

# The source file we read from - this is the raw data from the city
src_emissions_filename = 'ChicagoEnergyBenchmarking.csv'

# The output file we generate that has all columns, but just for the latest year reported
# TODO: Rename to -temp and put in a /temp directory to make clear this isn't being used by the final
# app, and is generated
newest_instances_out_filename = 'ChicagoEnergyBenchmarkingAllNewestInstances.csv'

# The output file we generate with limited columns but for ALL years (reported and non-reported),
# allowing us to track metrics (e.g. emissions, GHG intensity) over time, and reporting status
all_years_out_filename = 'benchmarking-all-years.csv'

# Columns that should be strings because they are immutable identifiers
string_cols = [
    'ChicagoEnergyRating',
    'ZIPCode',
    'Latitude',
    'Longitude'
]

# Int columns that are numbers (and can get averaged) but should be rounded
int_cols = [
    'NumberOfBuildings',
    'ENERGYSTARScore',
    # TODO: Move to string after figuring out why the X.0 is showing up
    'Wards',
    'CensusTracts',
    # 'ZIPCode',
    'CommunityAreas',
    'HistoricalWards2003-2015'
]

# The columns we want to have in our historical data output - we need the ID (to filter by a
# particular building) and should then have columns of interest that change over time (so yes to
# 'GHGIntensity', no to 'YearBuilt')
columns_to_track_over_time = [
    'ID',
    'DataYear',
    'ReportingStatus',
    'GrossFloorArea',
    'TotalGHGEmissions',
    'GHGIntensity',
    'NumberOfBuildings',
    'ChicagoEnergyRating',
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
]

replace_headers = {'Data Year': 'DataYear',
    'ID': 'ID',
    'Property Name': 'PropertyName',
    'Reporting Status': 'ReportingStatus',
    'Address': 'Address',
    'ZIP Code': 'ZIPCode',
    'Chicago Energy Rating': 'ChicagoEnergyRating',
    'Exempt From Chicago Energy Rating': 'ExemptFromChicagoEnergyRating',
    'Community Area': 'CommunityArea',
    'Primary Property Type': 'PrimaryPropertyType',
    'Gross Floor Area - Buildings (sq ft)': 'GrossFloorArea',
    'Total GHG Emissions (Metric Tons CO2e)': 'TotalGHGEmissions',
    'GHG Intensity (kg CO2e/sq ft)': 'GHGIntensity',
    'Year Built': 'YearBuilt',
    '# of Buildings': 'NumberOfBuildings',
    'Water Use (kGal)': 'WaterUse',
    'ENERGY STAR Score': 'ENERGYSTARScore',
    'Electricity Use (kBtu)': 'ElectricityUse',
    'Natural Gas Use (kBtu)': 'NaturalGasUse',
    'District Steam Use (kBtu)': 'DistrictSteamUse',
    'District Chilled Water Use (kBtu)': 'DistrictChilledWaterUse',
    'All Other Fuel Use (kBtu)': 'AllOtherFuelUse',
    'Site EUI (kBtu/sq ft)': 'SiteEUI',
    'Source EUI (kBtu/sq ft)': 'SourceEUI',
    'Weather Normalized Site EUI (kBtu/sq ft)': 'WeatherNormalizedSiteEUI',
    'Weather Normalized Source EUI (kBtu/sq ft)': 'WeatherNormalizedSourceEUI',
    'Latitude': 'Latitude',
    'Longitude': 'Longitude',
    'Location': 'Location',
    'Row_ID': 'Row_ID',
    'Wards': 'Wards',
    'Community Areas': 'CommunityAreas',
    'Zip Codes': 'ZipCodes',
    'Census Tracts': 'CensusTracts',
    'Historical Wards 2003-2015': 'HistoricalWards2003-2015' }

def rename_columns(building_data: pd.DataFrame) -> pd.DataFrame:
    return building_data.rename(columns=replace_headers)

def get_buildings_with_ghg_intensity(building_data: pd.DataFrame) -> pd.DataFrame:
    """Filter to buildings with a greenhouse gas intensity present, as otherwise it's likely empty
       or junk data"""

    return building_data.loc[(building_data['GHGIntensity'] > 0)].copy()

def get_submitted_data(building_data: pd.DataFrame) -> pd.DataFrame:
    """Filter down to building entries with reported data"""

    is_submitted = (building_data['ReportingStatus'] == 'Submitted')
    is_submitted_data = (building_data['ReportingStatus'] == 'Submitted Data')
    has_status_submitted = is_submitted | is_submitted_data

    return building_data.loc[has_status_submitted].copy()

def get_last_year_data(all_submitted_data: pd.DataFrame) -> pd.DataFrame:
    """ Filter down data to only the latest submission (reported year) per building"""
    all_submitted_data = all_submitted_data.sort_values(by=['ID', 'DataYear'])
    all_recent_submitted_data = all_submitted_data.drop_duplicates(subset=['ID'], keep='last').copy()
    return all_recent_submitted_data


def filter_cols_historic(building_data: pd.DataFrame) -> pd.DataFrame:
    """Filter down the reporting entries to only columns relevant to our historical data CSV"""

    return building_data[columns_to_track_over_time]

def fix_str_cols(all_recent_submitted_data: pd.DataFrame, renamed_building_data: pd.DataFrame) -> pd.DataFrame:
    """ Mark columns that look like numbers but should be strings as such to prevent decimals showing
     up (e.g. zipcode of 60614 or Ward 9) """
    all_recent_submitted_data[string_cols] = renamed_building_data[string_cols].astype('string')
    return all_recent_submitted_data

def fix_int_cols(building_data: pd.DataFrame) -> pd.DataFrame:
    building_data[int_cols] = building_data[int_cols].astype('Int64')
    return building_data

def output_to_csv(building_data: pd.DataFrame, dir: str) -> None:
    """ Mark columns as ints that should never show a decimal, e.g. Number of Buildings, Zipcode """
    building_data.to_csv(dir, sep=',', encoding='utf-8', index=False)

def process(file_path: str, latest_year_only: bool) -> pd.DataFrame:
    """Process an input file, renaming columns and applying filters based on whether we are getting
       only the latest year for each building or all historic data"""
    building_data = get_and_clean_csv(file_path)

    building_data = rename_columns(building_data)

    # Used to be fix_str_cols(cleaned_data, building_data) when this was below the filtering
    cleaned_data = fix_str_cols(building_data, building_data)
    cleaned_data = fix_int_cols(cleaned_data)

    # Only filter to the latest reporting year if that's the file we're generating
    if (latest_year_only):
        cleaned_data = get_buildings_with_ghg_intensity(building_data)
        cleaned_data = get_submitted_data(cleaned_data)
        cleaned_data = get_last_year_data(cleaned_data)
    else:
        cleaned_data = filter_cols_historic(cleaned_data)

    return cleaned_data

def main():
    processed_latest_year = process(get_data_file_path(file_dir, src_emissions_filename), True)
    processed_all_years = process(get_data_file_path(file_dir, src_emissions_filename), False)

    # Output the latest year data to source, since other processing steps still get applied
    output_to_csv(processed_latest_year, get_data_file_path(file_dir, newest_instances_out_filename))

    # The all years data is in it's final form already, we don't do ranks or stats off of it (yet)
    output_to_csv(processed_all_years, get_data_file_path(out_file_dir, all_years_out_filename))

if __name__ == '__main__':
    main()
