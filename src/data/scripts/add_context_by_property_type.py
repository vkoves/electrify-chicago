"""
A script that adds rankings to buildings by property type (e.g. #1 highest emissions of Office
buildings)
"""

import pandas as pd
import json

from typing import List, Union, Any, cast
from pandas.core.groupby.generic import DataFrameGroupBy
from src.data.scripts.utils import (
    get_data_file_path,
    log_step_completion,
    output_to_csv,
)
from src.data.scripts.building_utils import (
    benchmarking_string_cols,
    benchmarking_int_cols,
)

out_dir = "dist"

# Input file path (also written to)
input_benchmark_data_csv_path = get_data_file_path(out_dir, "building-benchmarks.csv")

# Output file paths
property_types_file_path = get_data_file_path(out_dir, "property-types.json")
property_stats_file_path = get_data_file_path(
    out_dir, "building-statistics-by-property-type.json"
)

# Columns we want to rank for and append ranks to each building's data
building_cols_to_rank = [
    "GHGIntensity",
    "TotalGHGEmissions",
    "ElectricityUse",
    "NaturalGasUse",
    "GrossFloorArea",
    "SourceEUI",
    "SiteEUI",
]


def generate_property_types(property_types: List[Any]) -> List[str]:
    """
    Output property_types to a json file for use in the frontend (like the type filter).
    Returns the file written to as an array
    """
    property_types_json = {"propertyTypes": property_types}

    with open(property_types_file_path, "w", encoding="latin1") as json_file:
        json.dump(property_types_json, json_file)

    return [property_types_file_path]


def calculate_building_stats(
    property_types: List[str], grouped_by_prop_type: DataFrameGroupBy
) -> str:
    """
    Calculates stats by property type (e.g. median GHG emissions) and writes them to JSON file

    Takes in the dictionary of property types from the grouped data, and the grouped data.

    Returns the file path written to
    """

    stats_by_property_type = {}

    # looping through both all the property types and all the columns we want to get data on
    for i, property in enumerate(property_types):
        cur_property_type_stats = {}
        cur_count = 0

        for col in building_cols_to_rank:
            # finding the mean, count, min, max, and quartiles of each category for each building type
            try:
                cur_count = int(grouped_by_prop_type[col].count().iloc[i])
                cur_min = round(float(grouped_by_prop_type[col].min().iloc[i]), 3)
                cur_max = round(float(grouped_by_prop_type[col].max().iloc[i]), 3)
                cur_first_quartile = round(float(grouped_by_prop_type[col].quantile(q=0.25).iloc[i]), 3)
                cur_median = round(float(grouped_by_prop_type[col].quantile(q=0.5).iloc[i]), 1)
                cur_third_quartile = round(float(grouped_by_prop_type[col].quantile(q=0.75).iloc[i]), 3)
            except (IndexError, AttributeError, ValueError):
                # Skip this property type/column combination if data is not available
                continue

            cur_property_type_stats[col] = {
                "count": cur_count,
                "min": cur_min,
                "max": cur_max,
                "twentyFifthPercentile": cur_first_quartile,
                "median": cur_median,
                "seventyFifthPercentile": cur_third_quartile,
            }

        if cur_count == 0:
            continue

        stats_by_property_type[property] = cur_property_type_stats

    with open(property_stats_file_path, "w") as property_stats_file:
        json.dump(stats_by_property_type, property_stats_file)

    return property_stats_file_path


def rank_buildings_by_property_type(
    building_data: pd.DataFrame,
    property_types: List[str],
    grouped_by_prop_type: DataFrameGroupBy,
) -> List[str]:
    """
    Ranks buildings in relation to their property type, then re-exporting the file

    Returns the file paths written to

    TODO: Investigate if this should use just the latest year buildings, because we don't want to
        rank a building that didn't report in the latest year against buildings of a different year
    """

    # calculates the statistics for building property types (e.g. average GHG intensity for Hotels)
    building_stats_path = calculate_building_stats(property_types, grouped_by_prop_type)

    # Mark columns that look like numbers but should be strings as such to prevent decimals showing
    # up (e.g. zipcode of 60614 or Ward 9) and make sure missing data is output as a string
    building_data[benchmarking_string_cols] = (
        building_data[benchmarking_string_cols].fillna("").astype(str)
    )

    # Mark columns as ints that should never show a decimal, e.g. Number of Buildings, Zipcode
    building_data[benchmarking_int_cols] = building_data[benchmarking_int_cols].astype(
        "Int64"
    )

    # use pandas to rank each value for each property and store as category+"RankByProperty"
    for col in building_cols_to_rank:
        building_data[col + "RankByPropertyType"] = grouped_by_prop_type[col].rank(
            ascending=False
        )

    output_to_csv(building_data, input_benchmark_data_csv_path)

    return [building_stats_path, input_benchmark_data_csv_path]


###
### Main
###
def main() -> None:
    # Read in benchmark data, which only contains one instance of each building
    building_data = pd.read_csv(input_benchmark_data_csv_path)

    # find the latest year
    latest_year = building_data["DataYear"].max()

    # Filter to data for the newest year, so we don't aggregate stats over all time
    latest_building_data = building_data[building_data["DataYear"] == latest_year]

    # sorted data based on each property type: the order is alphabetical
    grouped_by_prop_type = cast(DataFrameGroupBy, latest_building_data.groupby("PrimaryPropertyType"))

    # get a list of all unique property types
    property_types = [str(key) for key in grouped_by_prop_type.groups.keys()]

    outputted_paths = []
    outputted_paths += rank_buildings_by_property_type(
        building_data, property_types, grouped_by_prop_type
    )
    outputted_paths += generate_property_types(property_types)

    log_step_completion(3, outputted_paths)


if __name__ == "__main__":
    main()
