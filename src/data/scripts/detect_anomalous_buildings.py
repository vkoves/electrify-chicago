"""
A script that detects anomalous buildings, which we don't show grades for. Anomalies come from
trends in over time (e.g. an unusually quick decrease or increase), so we read the historic data to
detect anomalies but flag anomalous data in the main benchmark data set that only contains each
building once.

This includes:

- Natural Gas Reported 0 but Was Non-Zero Before (e.g. Moody Solheim Center as of 2022, ID 165717)
  These buildings score
"""

from typing import List, Optional
import pandas as pd

from src.data.scripts.utils import (
    get_data_file_path,
    log_step_completion,
    output_to_csv,
)
from src.data.scripts.building_utils import (
    benchmarking_string_cols,
    benchmarking_int_cols,
)


# Valid data anomaly values, which can be combined with commas in a string
# (e.g. "anomaly1,anomaly2") to be future proofed
anomaly_values = {
    "zero_gas_but_prev_use": "gas:zero-with-prev-use",
    "large_gas_swing": "gas:large-swings",
}

# The relative share of electric use that a building's gas use has to meet to be marked as
# having used gas (e.g. 5% is 0.05). This should apply as a safeguard to all types of gas anomaly
# checks, since going from 5% to 0% shouldn't be flagged, nor 0% to 5%
#
# Some examples we want this to exclude:
# - https://electrifychicago.net/building/55-e-monroe - has four years where gas was 1% of total
#   energy use, every other year was 0.
# - https://electrifychicago.net/building/222-n-la-salle-st - had one year where gas was 7% of total
#   energy use, every other year was less
gas_use_min_share_decimal = 0.10

out_dir = "dist"

# Input historic data from Step 1
input_historic_data_csv_path = get_data_file_path(out_dir, "benchmarking-all-years.csv")

# Output main benchmark path
input_benchmark_data_csv_path = get_data_file_path(out_dir, "building-benchmarks.csv")


def detect_gas_users(historic_data: pd.DataFrame) -> pd.DataFrame:
    """
    Identifies buildings that used a noticeable amount of natural gas relative to their electricity use.

    This function filters the historic data to identify buildings that used natural gas above a
    specified threshold (defaulting to 5% of their electricity use) in years prior to a given year.
    This helps distinguish notable gas usage (HVAC) that should not change rapidly from small uses
    like an industrial kitchen.

    Example: 55 E Monroe, which used gas in the past, but was < 1% of its total energy use, and
    should not be flagged.
    """

    # Handle cases where electricity use is zero to avoid division by zero errors
    used_gas_before = historic_data.loc[
        historic_data["NaturalGasUse"]
        > gas_use_min_share_decimal * historic_data["ElectricityUse"]
    ]

    return used_gas_before


def determine_abs_delta(x: pd.Series) -> Optional[float]:
    """
    Calculates the maximum absolute percentage change between consecutive values in a Pandas Series,
    ignoring series of just 0 and None.
    """

    # Check for empty or all-zero and NaN, as that means no change in our data (some buildings
    # report no Natural Gas, then 0)
    if x.empty or (x.dropna() == 0).all():
        return 0.0

    shifted_x = x.shift(1).fillna(x.iloc[0]) + 1
    delta = abs((x - shifted_x) / shifted_x).dropna()

    return delta.max()


def detect_large_gas_swing_buildings(
    historic_data: pd.DataFrame, threshold: float = 0.7
) -> List[int]:
    """
    Finds buildings in the given historic data DataFrame that sees reported gas use change greater
    than 100% in a given year in the past, as this is highly likely to be incorrect.
    The results are sorted from high to low.

    args:
        historic_data: the dataframe to analyze
        threshold: the percent threshold to detect buildings at (1 = 100%)

    returns:
        a list of building IDs that have anomalous gas use
    """

    # Ignore buildings with a very small share of gas use
    gas_users = detect_gas_users(historic_data)

    gas_grouped = gas_users.groupby("ID").agg({"NaturalGasUse": determine_abs_delta})

    # Ensure we have a DataFrame and reset index
    gas_df = pd.DataFrame(gas_grouped).reset_index()

    # Sort and filter
    anom_gas_usage = (
        gas_df.sort_values("NaturalGasUse", ascending=False)
        .dropna()
        .rename(columns={"NaturalGasUse": "NaturalGasChange"})
    )

    filtered_data = anom_gas_usage[anom_gas_usage.NaturalGasChange > threshold]
    anom_ids = pd.Series(filtered_data["ID"]).unique().tolist()

    thresh_prcnt = round(threshold * 100)
    print(
        f"- {len(anom_ids)} buildings with large (> {thresh_prcnt}%) swings in gas use."
    )

    return anom_ids


def detect_anomalous_zero_gas_buildings(historic_data: pd.DataFrame) -> List[int]:
    """
    Finds buildings in the given historic data DataFrame that reported 0 gas use in the latest year,
    (which we'd mark as gas free) but reported gas use in the past, as this is highly likely to be
    incorrect. Buildings that dip to 0 but come back are caught by our large swing detector.
    """

    latest_year = historic_data["DataYear"].max()

    no_gas_use_ids = (
        historic_data[(historic_data["NaturalGasUse"] == 0) | historic_data["NaturalGasUse"].isna()]
        .loc[historic_data["DataYear"] == latest_year]
    )['ID']

    # If a building used a noticeable amount of gas relative to its total energy use (for
    # simplicity, > 5% of their electric use), we flag it as having used gas. This prevents us
    # flagging buildings that went from using very little gas to zero, which is likely not an error,
    # but could come from an individual tenant using gas or only kitchens using gas and then going
    # electric
    old_records = historic_data.loc[historic_data["DataYear"] < latest_year]

    used_gas_in_past = detect_gas_users(old_records)

    gas_anomalies = used_gas_in_past.loc[historic_data["ID"].isin(no_gas_use_ids)]

    gas_anomaly_ids = gas_anomalies["ID"].unique().tolist()

    print(
        f"- {len(gas_anomaly_ids)} buildings with anomalous zero gas use in {latest_year}."
    )

    return gas_anomaly_ids


def find_and_note_anomalies(
    building_data: pd.DataFrame, historic_data: pd.DataFrame
) -> pd.DataFrame:
    """
    Calls our sub functions to find different types of anomalies and notates the anomalies they have
    in a new 'DataAnomalies' column that we add to the benchmark data, with formatted strings based
    off of our `anomaly_values`.

    Return a DataFrame with our new column
    """

    print("Found Anomalies:\n")

    zero_gas_anomaly_ids = detect_anomalous_zero_gas_buildings(historic_data)
    gas_swing_ids = detect_large_gas_swing_buildings(historic_data)

    print("")

    # Create the 'DataAnomalies' column and make it empty by default
    building_data["DataAnomalies"] = ""

    building_data.loc[building_data["ID"].isin(gas_swing_ids), "DataAnomalies"] = (
        anomaly_values["large_gas_swing"]
    )

    # Buildings that have reported 0 use and then a value will be a subset of the gas swing
    # buildings, but it's a more specific issue, so we mark it separately
    building_data.loc[
        building_data["ID"].isin(zero_gas_anomaly_ids), "DataAnomalies"
    ] = anomaly_values["zero_gas_but_prev_use"]

    return building_data


def detect_anomalous_buildings():
    """
    The main function to anomalous buildings, and notates the anomalies they have in a new 'DataAnomalies'
    column that we add to the benchmark data, with formatted strings based off of our `anomaly_keys`
    and `anomaly_values`
    """

    # Load in historic data for anomaly detection
    historic_data = pd.read_csv(input_historic_data_csv_path)

    # Load in full building data from previous step, where we store the anomaly data
    building_data = pd.read_csv(input_benchmark_data_csv_path)

    building_data = find_and_note_anomalies(building_data, historic_data)

    # Mark columns that look like numbers but should be strings as such to prevent decimals showing
    # up (e.g. zipcode of 60614 or Ward 9) and make sure missing data is output as a string
    building_data[benchmarking_string_cols] = (
        building_data[benchmarking_string_cols].fillna("").astype(str)
    )

    # Mark columns as ints that should never show a decimal, e.g. Number of Buildings, Zipcode
    building_data[benchmarking_int_cols] = building_data[benchmarking_int_cols].astype(
        "Int64"
    )

    output_to_csv(building_data, input_benchmark_data_csv_path)

    return [input_benchmark_data_csv_path]


###
### Main
###
def main() -> None:
    outputted_paths = []
    outputted_paths += detect_anomalous_buildings()

    log_step_completion(4, outputted_paths)


if __name__ == "__main__":
    main()
