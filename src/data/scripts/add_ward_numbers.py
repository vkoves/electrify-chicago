"""
add_ward_numbers takes in a DataFrame of buildings and adds ward numbers

Columns added:
'Ward': int
"""

import pandas as pd
from src.data.scripts.utils import get_data_file_path

# Pull City Geocoder data into a Data Frame
city_geocoder_path = get_data_file_path("source", "CityGeocoder.xlsx")
city_geocoder = pd.read_excel(city_geocoder_path)

def find_ward_number_by_city_geocoder(address: str) -> int | None:
    """Finds ward number for a given address provided by the city geocoder"""
    row = city_geocoder[city_geocoder["Address"] == address].iloc[0]
    ward_number = row['Wards (Current - 2023)']
    if ward_number == '---':
        return None
    return int(row["Wards (Current - 2023)"])

def add_ward_numbers(buildings: pd.DataFrame) -> pd.DataFrame:
    """ Generates geocodes and ward numbers in a Data Frame of buildings """
    # Find corresponding Ward number for each building based on benchmark data coordinates, using WardsShapes information
    # First based on benchmark data coordinates, then based on Google Maps Geocoding API coordinates
    buildings['Ward'] = buildings.apply(lambda building: find_ward_number_by_city_geocoder(building["Address"]), axis = 1)

    # Convert 'Ward' columns to int, handling any NaN values as -1
    buildings['Ward'] = buildings['Ward'].fillna(-1).astype(int)

    return buildings
