import pandas as pd
import pathlib
from shapely import Point, from_wkt

def calculate_ward_number(ward_shapes, currLong: int, currLat: int):
    currPoint = Point(currLong, currLat)
    if not currPoint:
        return None
    for index, ward in ward_shapes.iterrows():
        for shape in ward['ward_multipolygon'].geoms:
            if shape.contains(currPoint):
                return int(ward['Ward'])
    return None

def add_ward_numbers(buildings: pd.DataFrame) -> None:
    # Parse Ward shape from string (col: 'the_geom') to MultiPolygon (col: 'ward_multipolygon) in WardsShapes file
    curr_path = pathlib.Path(".")
    ward_path = curr_path.parent.absolute() / "src" / "data" / "source" / "WardsShapes.csv"
    ward_shapes = pd.read_csv(ward_path)
    ward_shapes['ward_multipolygon'] = ward_shapes.apply(lambda ward: from_wkt(ward.the_geom), axis = 1)

    # Find corresponding Ward number for each building, using WardsShapes information
    buildings['Ward'] = buildings.apply(lambda building: calculate_ward_number(ward_shapes, building.Longitude, building.Latitude), axis = 1)
    return buildings

# This file may be run by itself to test the add_ward_numbers function without saving the output
if __name__ == '__main__':
    curr_path = pathlib.Path(".")
    building_path = curr_path.parent.absolute() / "src" / "data" / "dist" / "building-benchmarks.csv"
    building_benchmarks = pd.read_csv(building_path)
    building_benchmarks = add_ward_numbers(building_benchmarks)
    print(building_benchmarks)