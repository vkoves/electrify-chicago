import pandas as pd
import json

path_to_property_type_json = "./dist/property-types.json"
path_to_buildings_csv = "./source/BenchmarkDataRenamed.csv"

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

building_data = pd.read_csv(path_to_buildings_csv)


def rankByType():
    building_data = pd.read_csv(path_to_buildings_csv)

    sorted_by_property_type = building_data.groupby("PrimaryPropertyType")

    for col in building_cols_to_rank:
        building_data[col +
                      'RankByPropertyType'] = sorted_by_property_type[col].rank(ascending=False)


df = pd.read_json(path_to_property_type_json)

building_data.to_json("./dist/test.json")
