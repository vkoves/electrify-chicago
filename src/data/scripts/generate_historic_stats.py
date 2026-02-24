"""

This script processes multi-year building energy benchmarking data to generate
comprehensive statistical summaries.  It transforms raw building energy data
into year-over-year statistical insights used for analysis and visualization.
"""

import math
import pandas
from typing import List, Dict
from src.data.scripts.utils import (
    get_and_clean_csv,
    get_data_file_path,
    log_step_completion,
    write_json_with_newline,
)

# DO NOT LEAVE TRUE ON `master`
debug = False

# Write out the data
output_filename = "historic-stats.json"

# Assume run in /data
data_directory = "source"
data_out_directory = "dist"

# The /debug directory is to have a well formatted JSON for reading
data_debug_directory = "debug"

# The input file from the previous step. Gatsby doesn't like spaces so we use a CSV with renamed
# headers with no units
building_emissions_file = "benchmarking-all-years.csv"

# The final output file name
building_emissions_file_out_name = "building-benchmarks"

# Columns we want to run statistical analysis and ranking on - order matters here
building_cols_to_analyze = [
    "GHGIntensity",
    "TotalGHGEmissions",
    "ElectricityUse",
    "NaturalGasUse",
    "SourceEUI",
    "SiteEUI",
    "DistrictSteamUse",
    "DistrictChilledWaterUse",
]


def clean_year_stats(stats_dict: dict) -> dict:
    """
    Post-processes a describe().to_dict() result:
    - Columns with count=0 are reduced to {"count": 0} to avoid NaN fields in JSON
    - NaN values in other columns are dropped (e.g. std=NaN for single-building years)
    - count is cast to int since buildings are always whole numbers
    """
    result = {}
    for col, col_stats in stats_dict.items():
        if col_stats.get("count", 0) == 0:
            result[col] = {"count": 0}
        else:
            result[col] = {
                k: int(v) if k == "count" else v
                for k, v in col_stats.items()
                if not (isinstance(v, float) and math.isnan(v))
            }
    return result


def hasReportedData(ghg_intensity) -> bool:
    """
    Determines if a building has reported data based on GHG Intensity.
    Matches the logic in common-functions.vue hasReportedData function.
    """
    return (
        pandas.notna(ghg_intensity)
        and isinstance(ghg_intensity, (int, float))
        and ghg_intensity > 0
    )


def calculateFirstAndLastYearReported(
    building_data: pandas.DataFrame,
) -> Dict[str, Dict[str, int]]:
    """
    Calculate FirstYearReported and LastYearReported for each building ID.

    Returns a dictionary mapping building ID to dict with FirstYearReported and LastYearReported.
    """
    reporting_years = {}

    # Group by ID and process each building
    for building_id, building_group in building_data.groupby("ID"):
        # Filter to rows with valid reported data
        reported_data = building_group[
            building_group["GHGIntensity"].apply(hasReportedData)
        ]

        if len(reported_data) > 0:
            years = sorted(reported_data["DataYear"].tolist())
            reporting_years[str(building_id)] = {
                "FirstYearReported": years[0],
                "LastYearReported": years[-1],
            }
        # If no valid data, we don't include this building in the output

    if debug:
        print(f"Calculated reporting years for {len(reporting_years)} buildings")
        # Show some examples
        for bid, years in list(reporting_years.items())[:5]:
            print(
                f"  Building {bid}: {years['FirstYearReported']} - {years['LastYearReported']}"
            )

    return reporting_years


# Calculates year-over-year stats for all buildings and outputs them into a keyed JSON file
def calculateBuildingStatsByYear(building_data_in: pandas.DataFrame) -> List[str]:
    """
    Calculates year-over-year stats for all buildings and outputs them into a keyed JSON file.
    Returns statistics for each year in the dataset.

    Returns an array of files written to
    """

    # Clone the input data to prevent manipulating it on accident
    building_data = building_data_in.copy()

    # The details columns we want to keep. Note that 50% = median
    detail_cols_to_keep = ["count", "mean", "std", "min", "max", "25%", "50%", "75%"]

    # Get all unique years in the dataset
    years = sorted(building_data["DataYear"].unique())

    # Dictionary to store results for each year
    yearly_stats = {}
    HISTORIC_DATA_START_YEAR = 2016

    for year in years:
        if year < HISTORIC_DATA_START_YEAR:
            continue

        # Filter data for this specific year
        year_data = building_data[building_data["DataYear"] == year]

        # Calculate statistics for this year
        year_stats_df = (
            year_data[building_cols_to_analyze].describe().loc[detail_cols_to_keep]  # type: ignore
        )

        # Round all data to 1 decimal place
        year_stats_df = year_stats_df.round(1)

        if debug:
            print("-" * 60)
            print(year)
            print(year_stats_df)

        # Rename columns to work with GraphQL (no numbers like '25%')
        year_stats_df.rename(
            index={
                "25%": "twentyFifthPercentile",
                "50%": "median",
                "75%": "seventyFifthPercentile",
            },
            inplace=True,
        )

        # Convert to dictionary and store
        yearly_stats[str(year)] = clean_year_stats(year_stats_df.to_dict())

    # Create summary statistics across all years

    if debug:
        print(f"\n{'=' * 50}")
        print("SUMMARY BY YEAR:")
        print(f"{'=' * 50}")
        print(
            f"{'Year':<6} {'Buildings':<10} {'Avg GHG':<12} {'Median GHG':<12} {'Avg Intensity':<12}"
        )
        print("-" * 60)

    for year in years:
        if year < HISTORIC_DATA_START_YEAR:
            continue

        year_stats = yearly_stats[str(year)]
        buildings = int(year_stats["TotalGHGEmissions"]["count"])
        avg_ghg = year_stats["TotalGHGEmissions"]["mean"]
        median_ghg = year_stats["TotalGHGEmissions"]["median"]
        avg_intensity = year_stats["GHGIntensity"]["mean"]

        if debug:
            print(
                f"{year:<6} {buildings:<10} {avg_ghg:<12.1f} {median_ghg:<12.1f} {avg_intensity:<12.1f}"
            )

    # Write output files
    stats_dist_output_path = get_data_file_path(data_out_directory, output_filename)
    stats_debug_output_path = str(
        get_data_file_path(data_debug_directory, output_filename)
    )

    # Write the minified JSON to the dist directory and indented JSON to the debug directory
    write_json_with_newline(yearly_stats, stats_dist_output_path)
    write_json_with_newline(yearly_stats, stats_debug_output_path, indent=4)

    return [stats_dist_output_path, stats_debug_output_path]


def main():
    # Read in the buildings data CSV from the previous pipeline step
    building_data = get_and_clean_csv(
        get_data_file_path(data_out_directory, building_emissions_file)
    )

    # Convert our columns to analyze to numeric data by stripping commas, otherwise the rankings are junk
    building_data[building_cols_to_analyze] = building_data[
        building_cols_to_analyze
    ].apply(
        lambda x: pandas.to_numeric(x.astype(str).str.replace(",", ""), errors="coerce")
    )

    # Calculate statistics by year for all buildings
    stats_files = calculateBuildingStatsByYear(building_data)

    log_step_completion(5, stats_files)


if __name__ == "__main__":
    main()
