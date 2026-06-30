"""
A script that compiles building emissions data at the ward level
"""

import pandas as pd

from src.data.scripts.utils import (
    get_data_file_path,
    log_step_completion,
    output_to_csv,
)

out_dir = "dist"

# Input file path (also written to)
input_benchmark_data_csv_path = get_data_file_path(out_dir, "building-benchmarks.csv")

# Output file paths
ward_stats_file_path = get_data_file_path(out_dir, "ward-stats.csv")


def calculate_compliant_buildings(
    building_data: pd.DataFrame,
    latest_year: int,
) -> pd.Series:
    compliant_counts = (
        building_data[building_data["DataYear"] == latest_year]
        .groupby("Ward")
        .size()
        .rename("Compliant Buildings")
    )

    return compliant_counts


def calculate_avg_building_age(
    building_data: pd.DataFrame,
    latest_year: int,
) -> pd.Series:
    age_df = building_data.dropna(subset=["YearBuilt"]).copy()
    age_df["age"] = latest_year - age_df["YearBuilt"]
    avg_age = age_df.groupby("Ward")["age"].mean().rename("Avg Building Age (years)")

    return avg_age


def compile_ward_stats(
    building_data: pd.DataFrame,
    compliant_counts: pd.Series,
    avg_age: pd.Series,
) -> pd.DataFrame:
    ward_stats = building_data.groupby("Ward").agg(
        **{
            "Total Buildings": ("Ward", "size"),
            "Total GHG Emissions (tons CO2 eq.)": ("TotalGHGEmissions", "sum"),
            "Avg GHG Intensity (kg CO2 eq./sqft)": ("GHGIntensity", "mean"),
            "Total Square Footage": ("GrossFloorArea", "sum"),
        }
    )

    ward_stats = ward_stats.join(compliant_counts).join(avg_age)
    ward_stats["Compliant Buildings"] = (
        ward_stats["Compliant Buildings"].fillna(0).astype(int)
    )

    ward_stats = ward_stats.reindex(range(1, 51)).reset_index()

    return ward_stats[
        [
            "Ward",
            "Compliant Buildings",
            "Total Buildings",
            "Total GHG Emissions (tons CO2 eq.)",
            "Avg GHG Intensity (kg CO2 eq./sqft)",
            "Total Square Footage",
            "Avg Building Age (years)",
        ]
    ]


###
### Main
###
def main() -> None:
    building_data = pd.read_csv(input_benchmark_data_csv_path)

    # find the latest year
    latest_year = int(building_data["DataYear"].max())

    compliant_counts = calculate_compliant_buildings(building_data, latest_year)

    avg_age = calculate_avg_building_age(building_data, latest_year)

    ward_stats = compile_ward_stats(building_data, compliant_counts, avg_age)

    # Output to CSV
    output_to_csv(ward_stats, ward_stats_file_path)

    log_step_completion(4, [ward_stats_file_path])


if __name__ == "__main__":
    main()
