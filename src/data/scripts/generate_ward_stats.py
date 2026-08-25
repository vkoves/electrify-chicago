"""
A script that compiles building emissions data at the ward level
"""

import pandas as pd

from typing import cast

from src.data.scripts.utils import (
    get_data_file_path,
    log_step_completion,
    output_to_csv,
)

COMPLIANT_BUILDINGS = "Compliant Buildings"
TOTAL_BUILDINGS = "Total Buildings"
TOTAL_GHG_EMISSIONS = "Total GHG Emissions (tons CO2 eq.)"
AVG_GHG_INTENSITY = "Avg GHG Intensity (kg CO2 eq./sqft)"
TOTAL_SQUARE_FOOTAGE = "Total Square Footage"
AVG_BUILDING_AGE = "Avg Building Age (years)"

out_dir = "dist"

# Input file path (also written to)
input_benchmark_data_csv_path = get_data_file_path(out_dir, "building-benchmarks.csv")

# Output file paths
ward_stats_file_path = get_data_file_path(out_dir, "ward-stats.csv")


def get_latest_year(
    building_data: pd.DataFrame,
) -> int:
    valid_years = building_data["DataYear"].dropna()
    if valid_years.empty:
        raise ValueError("No valid DataYear values found in building data")
    return int(valid_years.max())

"""
Uses the latest_year variable extracted from the most up-to-date
raw city data. Filters building data to rows matching the latest year reported,
then groups and aggregates the total per ward.
"""
def calculate_compliant_buildings(
    building_data: pd.DataFrame,
    latest_year: int,
) -> pd.Series:
    compliant_counts = (
        building_data[building_data["DataYear"] == latest_year].groupby("Ward").size()
    )
    compliant_counts.name = COMPLIANT_BUILDINGS

    return cast(pd.Series, compliant_counts)


def calculate_avg_building_age(
    building_data: pd.DataFrame,
    latest_year: int,
) -> pd.Series:
    age_df = building_data.dropna(subset=["YearBuilt"]).copy()
    age_df["age"] = latest_year - age_df["YearBuilt"]
    avg_age = age_df.groupby("Ward")["age"].mean()
    avg_age.name = AVG_BUILDING_AGE

    return cast(pd.Series, avg_age)


def compile_ward_stats(
    building_data: pd.DataFrame,
    compliant_counts: pd.Series,
    avg_age: pd.Series,
) -> pd.DataFrame:
    ward_stats = building_data.groupby("Ward").agg(
        **{
            TOTAL_BUILDINGS: ("Ward", "size"),
            TOTAL_GHG_EMISSIONS: ("TotalGHGEmissions", "sum"),
            AVG_GHG_INTENSITY: ("GHGIntensity", "mean"),
            TOTAL_SQUARE_FOOTAGE: ("GrossFloorArea", "sum"),
        }
    )

    ward_stats = ward_stats.join(compliant_counts).join(avg_age)

    ward_stats = cast(pd.DataFrame, ward_stats.reindex(range(1, 51))).reset_index()

    ward_stats[COMPLIANT_BUILDINGS] = (
        ward_stats[COMPLIANT_BUILDINGS].fillna(0).astype(int)
    )

    return cast(
        pd.DataFrame,
        ward_stats[
            [
                "Ward",
                COMPLIANT_BUILDINGS,
                TOTAL_BUILDINGS,
                TOTAL_GHG_EMISSIONS,
                AVG_GHG_INTENSITY,
                TOTAL_SQUARE_FOOTAGE,
                AVG_BUILDING_AGE,
            ]
        ],
    )


###
### Main
###
def main() -> None:
    building_data = pd.read_csv(input_benchmark_data_csv_path)

    # find the latest year
    latest_year = get_latest_year(building_data)

    compliant_counts = calculate_compliant_buildings(building_data, latest_year)

    avg_age = calculate_avg_building_age(building_data, latest_year)

    ward_stats = compile_ward_stats(building_data, compliant_counts, avg_age)

    # Output to CSV
    output_to_csv(ward_stats, ward_stats_file_path)

    log_step_completion(8, [ward_stats_file_path])


if __name__ == "__main__":
    main()
