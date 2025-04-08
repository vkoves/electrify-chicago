"""
Takes in a Data Frame of buildings and adds the buildings' ward number in 'Ward' column
"""

import pandas as pd
import pathlib
from shapely import Point, from_wkt
from src.data.scripts.utils import get_data_file_path

def find_ward_number(ward_shapes: pd.DataFrame, currLong: int, currLat: int) -> int | None:
    """
    Calculates the ward number for a given coordinate

    Takes in a coordinate

    Returns the Ward number, or None if it does not correspond to a ward
    """
    currPoint = Point(currLong, currLat)
    if not currPoint:
        return None
    for index, ward in ward_shapes.iterrows():
        for shape in ward['ward_multipolygon'].geoms:
            if shape.contains(currPoint):
                return int(ward['Ward'])
    return None

def add_ward_numbers(buildings: pd.DataFrame) -> pd.DataFrame:
    """ Generates ward numbers in a Data Frame of buildings """
    # Parse Ward shape from string (col: 'the_geom') to MultiPolygon (col: 'ward_multipolygon) in WardsShapes file
    ward_path = get_data_file_path("source", "WardsShapes.csv")
    ward_shapes = pd.read_csv(ward_path)
    ward_shapes['ward_multipolygon'] = ward_shapes.apply(lambda ward: from_wkt(ward.the_geom), axis = 1)

    # Find corresponding Ward number for each building, using WardsShapes information
    buildings['Ward'] = buildings.apply(lambda building: find_ward_number(ward_shapes, building.Longitude, building.Latitude), axis = 1)

    return buildings

# This file may be run by itself to test the add_ward_numbers function without saving the output
def main() -> None:
    # Read in building data from building benchmarks
    curr_path = pathlib.Path(".")
    building_path = curr_path.parent.absolute() / "src" / "data" / "dist" / "building-benchmarks.csv"
    building_benchmarks = pd.read_csv(building_path)

    # Add Ward numbers to building data and print
    building_benchmarks = add_ward_numbers(building_benchmarks)
    print(building_benchmarks)

if __name__ == '__main__':
    main()
