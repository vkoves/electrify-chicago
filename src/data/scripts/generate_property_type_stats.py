"""
A script that adds rankings to buildings by property type (e.g. #1 highest emissions of Office
buildings)
"""

import pandas as pd

from typing import List, Any, cast
from pandas.core.groupby.generic import DataFrameGroupBy
from src.data.scripts.utils import (
    get_data_file_path,
    log_step_completion,
    output_to_csv,
    write_json_with_newline,
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

# Columns for which we compute a total (sum) across all buildings of a property type
building_cols_to_total = [
    "TotalGHGEmissions",
    "GrossFloorArea",
    "ElectricityUse",
    "NaturalGasUse",
]

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

    write_json_with_newline(property_types_json, str(property_types_file_path))

    return [property_types_file_path]


def calculate_building_stats(
    property_types: List[str], grouped_by_prop_type: DataFrameGroupBy
) -> str:
    """
    Calculates stats by property type (e.g. median GHG emissions) and writes them to JSON file

    Takes in the dictionary of property types from the grouped data, and the grouped data.

    Returns the file path written to
    """

    # Stat rows from describe() to include (excludes std)
    detail_cols_to_keep = ["count", "mean", "min", "25%", "50%", "75%", "max"]
    rename_map = {
        "25%": "twentyFifthPercentile",
        "50%": "median",
        "75%": "seventyFifthPercentile",
    }

    # Compute all stats upfront
    describe_df = grouped_by_prop_type[building_cols_to_rank].describe()
    sum_df = grouped_by_prop_type[building_cols_to_total].sum()
    grade_dist = (
        grouped_by_prop_type["AvgPercentileLetterGrade"]
        .value_counts()
        .unstack(fill_value=0)
    )

    stats_by_property_type = {}

    for property in property_types:
        if property not in describe_df.index:
            continue

        # Build per-column stats from describe(), dropping columns with no data
        prop_df = (
            describe_df.loc[property]
            .unstack()[detail_cols_to_keep]
            .rename(columns=rename_map)
            .round(1)
        )
        prop_df = prop_df[prop_df["count"] > 0]
        prop_stats = prop_df.to_dict(orient="index")

        # Fix count to be int (describe() returns it as float)
        for col_stats in prop_stats.values():
            col_stats["count"] = int(col_stats["count"])

        # Add totals for aggregate fields needed by the property type page
        for col in building_cols_to_total:
            if col in prop_stats:
                prop_stats[col]["total"] = round(float(sum_df.loc[property, col]), 1)

        # Add grade distribution
        if property in grade_dist.index:
            prop_stats["gradeDistribution"] = {
                grade: int(count)
                for grade, count in grade_dist.loc[property].items()
                if count > 0
            }

        stats_by_property_type[property] = prop_stats

    write_json_with_newline(stats_by_property_type, str(property_stats_file_path))

    return property_stats_file_path


def rank_buildings_by_property_type(
    building_data: pd.DataFrame,
    grouped_by_prop_type: DataFrameGroupBy,
) -> List[str]:
    """
    Ranks buildings against others of the same property type using only the latest year's
    buildings, then re-exports the file.

    Returns the file paths written to
    """

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

    return [input_benchmark_data_csv_path]


###
### Main
###
def main() -> None:
    # Read in benchmark data, which only contains one instance of each building
    building_data = pd.read_csv(input_benchmark_data_csv_path)

    # find the latest year
    latest_year = building_data["DataYear"].max()

    # Filter to buildings that reported in the latest year - used for rankings and property type
    # list, so only currently active buildings appear
    latest_building_data = building_data[building_data["DataYear"] == latest_year]
    latest_year_grouped = cast(
        DataFrameGroupBy, latest_building_data.groupby("PrimaryPropertyType")
    )
    latest_property_types = [str(key) for key in latest_year_grouped.groups.keys()]

    # For stats, use all buildings at their latest reported year so totals and averages reflect
    # the full picture, not just buildings that happened to report in the most recent year
    all_buildings_grouped = cast(
        DataFrameGroupBy, building_data.groupby("PrimaryPropertyType")
    )
    all_property_types = [str(key) for key in all_buildings_grouped.groups.keys()]

    outputted_paths = []
    outputted_paths += [
        calculate_building_stats(all_property_types, all_buildings_grouped)
    ]
    outputted_paths += rank_buildings_by_property_type(
        building_data, latest_year_grouped
    )
    outputted_paths += generate_property_types(latest_property_types)

    log_step_completion(3, outputted_paths)


if __name__ == "__main__":
    main()
