"""
A script that adds rankings to buildings by property type (e.g. #1 highest emissions of Office
buildings)
"""

import pandas as pd
import json

from src.data.scripts.utils import get_data_file_path

out_dir = 'dist'
path_to_buildings_csv = get_data_file_path(out_dir, 'building-benchmarks.csv')
property_types_file_path = get_data_file_path(out_dir, 'property-types.json')
property_stats_file_path = get_data_file_path(out_dir, 'building-statistics-by-property-type.json')

# Columns we want to rank for and append ranks to each building's data
building_cols_to_rank = [
    'GHGIntensity',
    'TotalGHGEmissions',
    'ElectricityUse',
    'NaturalGasUse',
    'GrossFloorArea',
    'SourceEUI',
    'SiteEUI',
]

# Columns that should be strings because they are immutable identifiers
string_cols = [
    'ChicagoEnergyRating',
    'ZIPCode',
]

# Int columns that are numbers (and can get averaged) but should be rounded
int_cols = [
    'NumberOfBuildings',
    'ENERGYSTARScore',
    # TODO: Move to string after figuring out why the X.0 is showing up
    'Wards',
    'CensusTracts',
    'CommunityAreas',
    'HistoricalWards2003-2015'
]

# raw building data
building_data = pd.read_csv(path_to_buildings_csv)

# find the latest year
latest_year = building_data["DataYear"].max()

# filter just data for the max year
building_data = building_data[building_data["DataYear"] == latest_year]

# sorted data based on each property type: the order is alphabetical
sorted_by_property_type = building_data.groupby("PrimaryPropertyType")

# get a list of all unique property types
property_types = sorted_by_property_type.groups.keys()

# TODO: output property_types to a json file for use in the frontend
def generate_property_types():
    # output property_types to a json file for use in the frontend
    property_types_json = {"propertyTypes": list(property_types)}
    with open(property_types_file_path, 'w', encoding='latin1') as json_file:
        json.dump(property_types_json, json_file)

def calculateBuildingStatistics():
    stats_by_property_type = {}

    # looping through both all the property types and all the columns we want to get data on
    for i, property in enumerate(property_types):
        print("property", property)

        cur_property_type_stats = {}
        for col in building_cols_to_rank:

            # finding the mean, count, min, max, and quartiles of each category for each building type
            cur_count = sorted_by_property_type[col].count()[i].item()

            cur_min = round(sorted_by_property_type[col].min()[i].item(), 3)
            cur_max = round(sorted_by_property_type[col].max()[i].item(), 3)

            cur_first_quartile = round(
                sorted_by_property_type[col].quantile(q=0.25)[i].item(), 3)
            cur_median = round(
                sorted_by_property_type[col].quantile(q=0.5)[i].item(), 1)
            cur_third_quartile = round(
                sorted_by_property_type[col].quantile(q=0.75)[i].item(), 3)

            cur_property_type_stats[col] = {
                "count": cur_count,
                "min": cur_min,
                "max": cur_max,
                "twentyFifthPercentile": cur_first_quartile,
                "median": cur_median,
                "seventyFifthPercentile": cur_third_quartile
            }

        if cur_count == 0:
            continue

        stats_by_property_type[property] = cur_property_type_stats

    with open(property_stats_file_path, "w") as property_stats_file:
        json.dump(stats_by_property_type, property_stats_file)

# Ranks buildings in relation to their property type, then re-exporting the file
def rankBuildingsByPropertyType():
    # calculates the statistics for building property types (e.g. average GHG intensity for Hotels)
    calculateBuildingStatistics()

    # inputted data
    building_data = pd.read_csv(path_to_buildings_csv)

    # use pandas to rank each value for each property and store as category+"RankByProperty"
    for col in building_cols_to_rank:
        building_data[col +
                      'RankByPropertyType'] = sorted_by_property_type[col].rank(ascending=False)

    # Mark columns that look like numbers but should be strings as such to prevent decimals showing
    # up (e.g. zipcode of 60614 or Ward 9)
    building_data[string_cols] = building_data[string_cols].astype(str)

    # Mark columns as ints that should never show a decimal, e.g. Number of Buildings, Zipcode
    building_data[int_cols] = building_data[int_cols].astype('Int64')

    building_data.to_csv(path_to_buildings_csv, sep=',', encoding='utf-8', index=False)

if __name__ == "__main__":
    rankBuildingsByPropertyType()
    generate_property_types()
