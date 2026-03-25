"""
The initial processing file for the Electrify Chicago Data pipeline (Step 1 of 3 in data pipeline)

Ingests the initial city data CSV and renames its column headers for GraphQL compatibility in
Gridsome, and outputs two files into the dist/ directory, one with a limited number of columns
across all years (our historic data) and one with all columns for the latest year.

This is done because we only show historic data on individual building pages, and loading the
historic data on pages like search and the homepage would get quite heavy.
"""

import json
from pyproj import Transformer
from shapely.geometry import shape
import pandas as pd
from src.data.scripts.utils import (
    get_and_clean_csv,
    get_data_file_path,
    log_step_completion,
    output_to_csv,
)
from src.data.scripts.building_utils import (
    benchmarking_string_cols,
    benchmarking_int_cols,
)

file_dir = "source"
out_file_dir = "dist"
debug_file_dir = "debug"

# The source file we read from - this is the raw data from the city
src_emissions_filename = "ChicagoEnergyBenchmarking.csv"

# TODO : probably change filename and variable name for clarity and consistency
# The geoJSON file we use to replace erroneous coordinates from the city's raw data
src_verified_coordinates_filename = "d_chicago_energy_benchmark_buildings_permanent_20240115.geojson"

# The output file we generate that has all columns, but just for the latest year reported, which
# goes into the next step of the data pipeline
newest_instances_out_filename = "benchmarking-all-newest-temp.csv"

# The output file we generate with limited columns but for ALL years (reported and non-reported),
# allowing us to track metrics (e.g. emissions, GHG intensity) over time, and reporting status
all_years_out_filename = "benchmarking-all-years.csv"

# The columns we want to have in our historical data output - we need the ID (to filter by a
# particular building) and should then have columns of interest that change over time (so yes to
# 'GHGIntensity', no to 'YearBuilt')
columns_to_track_over_time = [
    "ID",
    "DataYear",
    "ReportingStatus",
    "GrossFloorArea",
    "TotalGHGEmissions",
    "GHGIntensity",
    "NumberOfBuildings",
    "ChicagoEnergyRating",
    "ENERGYSTARScore",
    "ElectricityUse",
    "NaturalGasUse",
    "DistrictSteamUse",
    "DistrictChilledWaterUse",
    "AllOtherFuelUse",
    "SiteEUI",
    "SourceEUI",
    "WeatherNormalizedSiteEUI",
    "WeatherNormalizedSourceEUI",
]

replace_headers = {
    "Data Year": "DataYear",
    "ID": "ID",
    "Property Name": "PropertyName",
    "Reporting Status": "ReportingStatus",
    "Address": "Address",
    "ZIP Code": "ZIPCode",
    "Chicago Energy Rating": "ChicagoEnergyRating",
    "Exempt From Chicago Energy Rating": "ExemptFromChicagoEnergyRating",
    "Community Area": "CommunityArea",
    "Primary Property Type": "PrimaryPropertyType",
    "Gross Floor Area - Buildings (sq ft)": "GrossFloorArea",
    "Total GHG Emissions (Metric Tons CO2e)": "TotalGHGEmissions",
    "GHG Intensity (kg CO2e/sq ft)": "GHGIntensity",
    "Year Built": "YearBuilt",
    "# of Buildings": "NumberOfBuildings",
    "Water Use (kGal)": "WaterUse",
    "ENERGY STAR Score": "ENERGYSTARScore",
    "Electricity Use (kBtu)": "ElectricityUse",
    "Natural Gas Use (kBtu)": "NaturalGasUse",
    "District Steam Use (kBtu)": "DistrictSteamUse",
    "District Chilled Water Use (kBtu)": "DistrictChilledWaterUse",
    "All Other Fuel Use (kBtu)": "AllOtherFuelUse",
    "Site EUI (kBtu/sq ft)": "SiteEUI",
    "Source EUI (kBtu/sq ft)": "SourceEUI",
    "Weather Normalized Site EUI (kBtu/sq ft)": "WeatherNormalizedSiteEUI",
    "Weather Normalized Source EUI (kBtu/sq ft)": "WeatherNormalizedSourceEUI",
    "Latitude": "Latitude",
    "Longitude": "Longitude",
    "Location": "Location",
    "Row_ID": "Row_ID",
    # 'Wards': 'Wards',
    # 'Community Areas': 'CommunityAreas',
    # 'Zip Codes': 'ZipCodes',
    # 'Census Tracts': 'CensusTracts',
    # 'Historical Wards 2003-2015': 'HistoricalWards2003-2015'
}


def rename_columns(building_data: pd.DataFrame) -> pd.DataFrame:
    return building_data.rename(columns=replace_headers)

def parse_geojson_field(value) -> dict | None:
    """ Helper function to parse coordinates when geojson property is 
    provided as a String """
    if not value:
        return None
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except (json.JSONDecodeError, ValueError):
            return None
    return value if isinstance(value, dict) else None

def apply_verified_coordinates(building_data: pd.DataFrame, geojson_path: str) -> pd.DataFrame:
    """ Parse through geoJSON data to extract proper coordinates for buildings """

    geojson_path = get_data_file_path(file_dir, geojson_path)

    """ TODO: Refactor into separate function? """
    # To use if properties.geojson.coordinates are not provided for a building
    # Takes IL State Plane feet from geometry.coordinates & converts to lon, lat
    transformer = Transformer.from_crs("EPSG:3435", "EPSG:4326", always_xy=True)

    with open(geojson_path, 'r') as f:
        geojson = json.load(f)
    
    verified_coords = {}
    for feature in geojson['features']:
        props = feature['properties']
        building_id = int(props['building_id'])

        """ TODO: Discuss with team about refactoring this logic into separate helper function """
        # Prefer WGS84 (lon, lat) coordinates if available
        geojson_val = parse_geojson_field(props.get('geojson')) # Check if string and return data we can parse
        if geojson_val and geojson_val.get('coordinates'):
            geom_type = geojson_val['type']
            if geom_type == 'Point':
                lon, lat = geojson_val['coordinates'] # GeoJSON is [lon, lat]
            else:
                # For Polygon/Multipolygon, use shapely to get centroid
                lon, lat = shape(geojson_val).centroid.coords[0]
            verified_coords[building_id] = (lat, lon)
        
        # Else, convert IL state plane units
        elif feature.get('geometry') and feature['geometry'].get('coordinates'):
            geom_type = feature['geometry']['type']
            if geom_type == 'Point':
                x, y = feature['geometry']['coordinates']
            else:
                # For Polygon/MultiPolygon, use shapely to get centroid
                x, y = shape(feature['geometry']).centroid.coords[0]
            lon, lat = transformer.transform(x, y) # Transform output is [lon, lat]
            verified_coords[building_id] = (lat, lon)
        

    # Override only where verified data exists
    def override_lat(row):
        bid = int(row['ID']) if pd.notna(row['ID']) else None
        return verified_coords[bid][0] if bid in verified_coords else row['Latitude']
    
    def override_lon(row):
        bid = int(row['ID']) if pd.notna(row['ID']) else None
        return verified_coords[bid][1] if bid in verified_coords else row['Longitude']

    def override_location(row):
        bid = int(row['ID']) if pd.notna(row['ID']) else None
        if bid in verified_coords:
            lat, lon = verified_coords[bid]
            return f"({lat}, {lon})"
        return row['Location']

    building_data['Latitude'] = building_data.apply(override_lat, axis=1)
    building_data['Longitude'] = building_data.apply(override_lon, axis=1)
    building_data['Location'] = building_data.apply(override_location, axis=1)

    return building_data

def get_buildings_with_ghg_intensity(building_data: pd.DataFrame) -> pd.DataFrame:
    """Filter to buildings with a greenhouse gas intensity present, as otherwise it's likely empty
    or junk data"""

    return building_data.loc[(building_data["GHGIntensity"] > 0)].copy()


def get_submitted_data(building_data: pd.DataFrame) -> pd.DataFrame:
    """Filter down to building entries with reported data"""

    is_submitted = building_data["ReportingStatus"] == "Submitted"
    is_submitted_data = building_data["ReportingStatus"] == "Submitted Data"
    has_status_submitted = is_submitted | is_submitted_data

    return building_data.loc[has_status_submitted].copy()


def get_last_year_data(all_submitted_data: pd.DataFrame) -> pd.DataFrame:
    """Filter down data to only the latest submission (reported year) per building"""
    all_submitted_data = all_submitted_data.sort_values(by=["ID", "DataYear"])
    all_recent_submitted_data = all_submitted_data.drop_duplicates(
        subset=["ID"], keep="last"
    ).copy()
    return all_recent_submitted_data


def filter_cols_historic(building_data: pd.DataFrame) -> pd.DataFrame:
    """Filter down the reporting entries to only columns relevant to our historical data CSV"""

    filtered_data = building_data[columns_to_track_over_time]
    # Ensure we always return a DataFrame, not a Series
    if isinstance(filtered_data, pd.Series):
        return filtered_data.to_frame().T
    return filtered_data


def fix_str_cols(
    all_recent_submitted_data: pd.DataFrame, renamed_building_data: pd.DataFrame
) -> pd.DataFrame:
    """Mark columns that look like numbers but should be strings as such to prevent decimals showing
    up (e.g. zipcode of 60614 or Ward 9)"""
    all_recent_submitted_data[benchmarking_string_cols] = renamed_building_data[
        benchmarking_string_cols
    ].astype("string")
    return all_recent_submitted_data


def fix_int_cols(building_data: pd.DataFrame) -> pd.DataFrame:
    building_data[benchmarking_int_cols] = building_data[benchmarking_int_cols].astype(
        "Int64"
    )
    return building_data


def process(file_path: str, latest_year_only: bool) -> pd.DataFrame:
    """Process an input file, renaming columns and applying filters based on whether we are getting
    only the latest year for each building or all historic data"""
    building_data = get_and_clean_csv(file_path)

    building_data = rename_columns(building_data)

    """ TODO: Likely move/re-work this further. 
    Is this the correct place in the data processing pipeline to apply this fix? 
    """
    # Fix any incorrect coordinate data
    if latest_year_only:
        building_data = apply_verified_coordinates(building_data, src_verified_coordinates_filename)

    # Used to be fix_str_cols(cleaned_data, building_data) when this was below the filtering
    cleaned_data = fix_str_cols(building_data, building_data)
    cleaned_data = fix_int_cols(cleaned_data)

    # Only filter to the latest reporting year if that's the file we're generating
    if latest_year_only:
        cleaned_data = get_buildings_with_ghg_intensity(building_data)
        cleaned_data = get_submitted_data(cleaned_data)
        cleaned_data = get_last_year_data(cleaned_data)
    else:
        cleaned_data = filter_cols_historic(cleaned_data)

    return cleaned_data


def main() -> None:
    processed_latest_year = process(
        get_data_file_path(file_dir, src_emissions_filename), True
    )
    processed_all_years = process(
        get_data_file_path(file_dir, src_emissions_filename), False
    )

    newest_out_path = get_data_file_path(debug_file_dir, newest_instances_out_filename)
    all_years_out_path = get_data_file_path(out_file_dir, all_years_out_filename)

    # Output the latest year data to source, since other processing steps still get applied
    output_to_csv(processed_latest_year, newest_out_path)

    # The all years data is in it's final form already, we don't do ranks or stats off of it (yet)
    output_to_csv(processed_all_years, all_years_out_path)

    log_step_completion(1, [newest_out_path, all_years_out_path])


if __name__ == "__main__":
    main()
