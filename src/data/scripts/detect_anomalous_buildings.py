"""
A script that detects anomalous buildings, which we don't show grades for. Anomalies come from
trends in over time (e.g. an unusually quick decrease or increase), so we read the historic data to
detect anomalies but flag anomalous data in the main benchmark data set that only contains each
building once.

This includes:

- Natural Gas Reported 0 but Was Non-Zero Before (e.g. Moody Solheim Center as of 2022, ID 165717)
  These buildings score
"""

from typing import List
import pandas as pd

from src.data.scripts.utils import get_data_file_path, log_step_completion, output_to_csv
from src.data.scripts.building_utils import benchmarking_string_cols, benchmarking_int_cols


# Valid data anomaly values, which can be combined with commas in a string
# (e.g. "anomaly1,anomaly2") to be future proofed
anomaly_values = {
    'zero_gas_but_prev_use': 'gas:zero-with-prev-use'
}

out_dir = 'dist'

# Input historic data from Step 1
input_historic_data_csv_path = get_data_file_path(out_dir, 'benchmarking-all-years.csv')

# Output main benchmark path
input_benchmark_data_csv_path = get_data_file_path(out_dir, 'building-benchmarks.csv')

def detect_anomalous_zero_gas_buildings(historic_data: pd.DataFrame) -> List[int]:
    """
    Finds buildings in the given historic data DataFrame that reported 0 gas use in any year, but
    reported gas use in the past, as this is highly likely to be incorrect.
    """

    latest_year = historic_data['DataYear'].max()

    no_gas_use = historic_data[historic_data['NaturalGasUse'] == 0]

    no_gas_use_ids = no_gas_use['ID']
    used_gas_before = historic_data.loc[historic_data['DataYear'] < latest_year].loc[historic_data['NaturalGasUse'] > 0]

    gas_anomalies = used_gas_before.loc[historic_data['ID'].isin(no_gas_use_ids)]

    gas_anomaly_ids = gas_anomalies['ID'].unique().tolist()

    print(f"Found {len(gas_anomaly_ids)} buildings with anomalous zero gas use.\n");

    return gas_anomaly_ids


def find_and_note_anomalies(building_data: pd.DataFrame, historic_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calls our sub functions to find different types of anomalies and notates the anomalies they have
    in a new 'DataAnomalies' column that we add to the benchmark data, with formatted strings based
    off of our `anomaly_values`.

    Return a DataFrame with our new column
    """
    zero_gas_anomaly_ids = detect_anomalous_zero_gas_buildings(historic_data)

    # Create the 'DataAnomalies' column and make it empty by default
    building_data['DataAnomalies'] = ''

    zero_gas_anomaly_val = anomaly_values['zero_gas_but_prev_use']

    building_data.loc[building_data['ID'].isin(zero_gas_anomaly_ids), 'DataAnomalies'] = zero_gas_anomaly_val

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
    building_data[benchmarking_string_cols] = building_data[benchmarking_string_cols].fillna('').astype(str)

    # Mark columns as ints that should never show a decimal, e.g. Number of Buildings, Zipcode
    building_data[benchmarking_int_cols] = building_data[benchmarking_int_cols].astype('Int64')

    output_to_csv(building_data, input_benchmark_data_csv_path)

    return [ input_benchmark_data_csv_path ]


###
### Main
###
def main() -> None:
    outputted_paths = []
    outputted_paths += detect_anomalous_buildings()

    log_step_completion(4, outputted_paths)

if __name__ == "__main__":
    main()
