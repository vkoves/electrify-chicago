import pandas as pd
from src.data.scripts.utils import get_and_clean_csv, get_data_file_path

file_dir = 'source'
building_emissions_file = 'ChicagoEnergyBenchmarking.csv'
data_out_file = 'ChicagoEnergyBenchmarkingAllNewestInstances.csv'

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

def get_all_ghg_data(building_data: pd.DataFrame) -> pd.DataFrame:
    return building_data.loc[(building_data['GHGIntensity'] > 0)].copy()

def get_submitted_data(building_data: pd.DataFrame) -> pd.DataFrame:
    is_submitted = (building_data['ReportingStatus'] == 'Submitted')
    is_submitted_data = (building_data['ReportingStatus'] == 'Submitted Data')
    has_status_submitted = is_submitted | is_submitted_data
    return building_data.loc[has_status_submitted].copy()

def get_last_year_data(all_submitted_data: pd.DataFrame) -> pd.DataFrame:
    all_submitted_data = all_submitted_data.sort_values(by=['ID', 'DataYear'])
    all_recent_submitted_data = all_submitted_data.drop_duplicates(subset=['ID'], keep='last').copy()
    return all_recent_submitted_data

def fix_str_cols(all_recent_submitted_data: pd.DataFrame, renamed_building_data: pd.DataFrame) -> pd.DataFrame:
    # Mark columns that look like numbers but should be strings as such to prevent decimals showing
    # up (e.g. zipcode of 60614 or Ward 9)
    all_recent_submitted_data[string_cols] = renamed_building_data[string_cols].astype('string')
    return all_recent_submitted_data

def fix_int_cols(building_data: pd.DataFrame) -> pd.DataFrame:
    building_data[int_cols] = building_data[int_cols].astype('Int64')
    return building_data

def output_to_csv(building_data: pd.DataFrame, dir: str) -> None:
    # Mark columns as ints that should never show a decimal, e.g. Number of Buildings, Zipcode
    building_data.to_csv(dir, sep=',', encoding='utf-8', index=False)

def process(file_path: str) -> pd.DataFrame:
    building_data = pd.read_csv(file_path, dtype='str')
    
    building_data = rename_columns(building_data)

    all_ghg_data = get_all_ghg_data(building_data)

    all_submitted_data = get_submitted_data(all_ghg_data)

    all_recent_submitted_data = get_last_year_data(all_submitted_data)

    all_recent_submitted_data = fix_str_cols(all_recent_submitted_data, building_data)
    
    all_recent_submitted_data = fix_int_cols(all_recent_submitted_data)

    return all_recent_submitted_data

def main():
    processed = process(get_data_file_path(file_dir, building_emissions_file))
    output_to_csv(processed, get_data_file_path(file_dir, data_out_file))

if __name__ == '__main__':
    main()
    