"""
add_ward_numbers takes in a DataFrame of buildings and adds ward numbers

Columns added:
'Ward': int
'WardMethod': 'City Geocoder' | 'Ward Boundaries and GMaps Coordinates'
"""

import pandas as pd
import pathlib
from shapely import Point, from_wkt
from src.data.scripts.utils import get_data_file_path

# Pull City Geocoder data into a Data Frame
city_geocoder_path = get_data_file_path("source", "CityGeocoder.xlsx")
city_geocoder = pd.read_excel(city_geocoder_path)

# Pull Building Coordinates into a Data Frame
building_coordinates_path = get_data_file_path("source", "BuildingCoordinates.csv")
building_coordinates = pd.read_csv(building_coordinates_path)

# Parse Ward shape from string (col: 'the_geom') to MultiPolygon (col: 'ward_multipolygon) in WardsShapes file
ward_path = get_data_file_path("source", "WardsShapes.csv")
ward_shapes = pd.read_csv(ward_path)
ward_shapes['ward_multipolygon'] = ward_shapes.apply(lambda ward: from_wkt(ward.the_geom), axis = 1)

def find_ward_number_by_city_geocoder(address: str) -> int | None:
    """Finds ward number for a given address provided by the city geocoder"""
    row = city_geocoder[city_geocoder["Address"] == address].iloc[0]
    ward_number = row['Wards (Current - 2023)']
    if ward_number == '---':
        return None
    return int(row["Wards (Current - 2023)"])

def find_ward_number_by_obj_coordinates(ward_shapes: pd.DataFrame, coordinatesStr: str) -> int | None:
    """Finds ward number for a given coordinate based on city ward shape files"""
    coordinates = eval(coordinatesStr)
    currLong = coordinates['longitude']
    currLat = coordinates['latitude']
    currPoint = Point(currLong, currLat)
    if not currPoint:
        return None
    for index, ward in ward_shapes.iterrows():
        for shape in ward['ward_multipolygon'].geoms:
            if shape.contains(currPoint):
                return int(ward['Ward'])
    return None

def find_ward_number_by_point_coordinates(ward_shapes: pd.DataFrame, lat: float, long: float) -> int | None:
    """Finds ward number for a given coordinate based on city ward shape files"""
    currPoint = Point(long, lat)
    if not currPoint:
        return None
    for index, ward in ward_shapes.iterrows():
        for shape in ward['ward_multipolygon'].geoms:
            if shape.contains(currPoint):
                return int(ward['Ward'])
    return None

def compare_ward_methods(building: pd.DataFrame) -> int:
    '''
    Test function that compares Ward number methods
    Output Key:
        >0: All methods produced the same Ward number
        -2: Odd one out is BenchmarkingCoord
        -3: Odd one out is GMaps
        -4: Odd one out is CityGeo
        -5: None returns
    '''
    if building['WardByCityGeocoder'] == building['WardByGMapsCoordinates'] and building['WardByCityGeocoder'] == building['WardByBenchmarkingCoordinates']:
        return building['WardByCityGeocoder']
    elif building['WardByCityGeocoder'] != building['WardByGMapsCoordinates'] and building['WardByCityGeocoder'] != building['WardByBenchmarkingCoordinates']:
       return -5
    elif building['WardByCityGeocoder'] == building['WardByGMapsCoordinates']:
        return -2
    elif building['WardByCityGeocoder'] == building['WardByBenchmarkingCoordinates']:
        return -3
    elif building['WardByGMapsCoordinates'] == building['WardByGMapsCoordinates']:
        return -4
    return -5

def add_ward_numbers(buildings: pd.DataFrame) -> pd.DataFrame:
    """ Generates geocodes and ward numbers in a Data Frame of buildings """
    # Find corresponding Ward number for each building based on benchmark data coordinates, using WardsShapes information
    # First based on benchmark data coordinates, then based on Google Maps Geocoding API coordinates
    buildings['Ward'] = buildings.apply(lambda building: find_ward_number_by_city_geocoder(building["Address"]), axis = 1)

    # Convert 'Ward' columns to int, handling any NaN values as -1
    buildings['Ward'] = buildings['Ward'].fillna(-1).astype(int)

    # Add coordinates to buildings
    buildings = pd.merge(buildings, building_coordinates, how="left", on="Address")

    # Find corresponding Ward number for each building based on benchmark data coordinates, using WardsShapes information
    # First based on benchmark data coordinates, then based on Google Maps Geocoding API coordinates
    # buildings['WardByGMapsCoordinates'] = buildings.apply(lambda building: find_ward_number_by_obj_coordinates(ward_shapes, building["Coordinates"]), axis = 1)

    # Convert 'Ward' and 'CalculatedWard' columns to int, handling any NaN values
    # buildings['WardByGMapsCoordinates'] = buildings['WardByGMapsCoordinates'].fillna(-1).astype(int)

    # Find corresponding Ward number for each building based on benchmark data coordinates, using WardsShapes information
    # First based on benchmark data coordinates, then based on Google Maps Geocoding API coordinates
    # buildings['WardByBenchmarkingCoordinates'] = buildings.apply(lambda building: find_ward_number_by_point_coordinates(ward_shapes, building["Latitude"], building["Longitude"]), axis = 1)

    # Convert 'Ward' and 'CalculatedWard' columns to int, handling any NaN values
    # buildings['WardByBenchmarkingCoordinates'] = buildings['WardByBenchmarkingCoordinates'].fillna(-1).astype(int)

    return buildings
