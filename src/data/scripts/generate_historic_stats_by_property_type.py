"""
Generates year-over-year statistics grouped by property type, producing
historic-stats-by-property-type.json for use in property type trend analysis.

Follows the same structure as generate_historic_stats.py but adds a property
type dimension, so the frontend can show trends for e.g. "Office" buildings
over time.
"""

import pandas
from src.data.scripts.utils import (
    get_and_clean_csv,
    get_data_file_path,
    log_step_completion,
    write_json_with_newline,
)
from src.data.scripts.generate_historic_stats import building_cols_to_analyze, clean_year_stats

output_filename = "historic-stats-by-property-type.json"
data_out_directory = "dist"
data_debug_directory = "debug"
building_emissions_file = "benchmarking-all-years.csv"
# PrimaryPropertyType lives here; we join it onto the all-years data by ID
building_benchmarks_file = "building-benchmarks.csv"

HISTORIC_DATA_START_YEAR = 2016


def calculate_historic_stats_by_property_type(
    building_data: pandas.DataFrame,
) -> list[str]:
    """
    Calculates year-over-year stats for each property type and outputs to JSON.

    Output structure:
      { "Office": { "2016": { "GHGIntensity": { ... }, ... }, "2017": { ... } }, ... }

    Returns a list of file paths written.
    """
    detail_cols_to_keep = ["count", "mean", "std", "min", "max", "25%", "50%", "75%"]
    rename_map = {
        "25%": "twentyFifthPercentile",
        "50%": "median",
        "75%": "seventyFifthPercentile",
    }

    years = sorted(building_data["DataYear"].unique())
    property_types = sorted(building_data["PrimaryPropertyType"].dropna().unique())

    stats_by_property_type = {}

    for property_type in property_types:
        prop_data = building_data[building_data["PrimaryPropertyType"] == property_type]
        yearly_stats = {}

        for year in years:
            if year < HISTORIC_DATA_START_YEAR:
                continue

            year_data = prop_data[prop_data["DataYear"] == year]

            if year_data.empty:
                continue

            year_stats_df = (
                year_data[building_cols_to_analyze]
                .describe()
                .loc[detail_cols_to_keep]
                .round(1)
                .rename(index=rename_map)
            )

            yearly_stats[str(year)] = clean_year_stats(year_stats_df.to_dict())

        if yearly_stats:
            stats_by_property_type[property_type] = yearly_stats

    dist_path = get_data_file_path(data_out_directory, output_filename)
    debug_path = get_data_file_path(data_debug_directory, output_filename)

    write_json_with_newline(stats_by_property_type, str(dist_path))
    write_json_with_newline(stats_by_property_type, str(debug_path), indent=4)

    return [dist_path, debug_path]


###
### Main
###
def main() -> None:
    building_data = get_and_clean_csv(
        get_data_file_path(data_out_directory, building_emissions_file)
    )

    # Convert columns to numeric, stripping commas from formatted numbers
    building_data[building_cols_to_analyze] = building_data[
        building_cols_to_analyze
    ].apply(
        lambda x: pandas.to_numeric(x.astype(str).str.replace(",", ""), errors="coerce")
    )

    # PrimaryPropertyType is only in building-benchmarks.csv (latest year per building).
    # Join it onto the all-years data by ID so we can group historic data by property type.
    benchmarks = pandas.read_csv(
        get_data_file_path(data_out_directory, building_benchmarks_file),
        usecols=["ID", "PrimaryPropertyType"],
    )
    building_data = building_data.merge(benchmarks, on="ID", how="left")

    output_files = calculate_historic_stats_by_property_type(building_data)

    log_step_completion(7, output_files)


if __name__ == "__main__":
    main()
