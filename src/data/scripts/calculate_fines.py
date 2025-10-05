"""
A script that calculates an estimated amount of fines the city could have collected during each year of reporting, under
the assumption the buildings that didn't comply would have not complied that whole year.

The fines by year and total get written to fines-by-year.json
"""

import json
from src.data.scripts.utils import get_and_clean_csv, get_data_file_path, log_step_completion

# THe maximum fine a building would get from not complying in a year, from the official ordinance
ANNUAL_MAX_FINE = 9200

# We use the historic data (benchmarking all years) to get years that were and were not submitted
historic_data_in_filename = 'benchmarking-all-years.csv'

output_filename = 'fines-by-year.json'

# Assume run in /data
data_out_directory = 'dist'

def calculate_fines() -> str:
    """
    Calculates fines that could have been collected

    Returns an array of files written to
    """

    # Read the built historic data
    historic_data = get_and_clean_csv(get_data_file_path(data_out_directory, historic_data_in_filename))

    not_submitted = historic_data[historic_data['ReportingStatus'] == 'Not Submitted']

    yearly_counts = not_submitted.groupby('DataYear').size()
    yearly_fines = yearly_counts * ANNUAL_MAX_FINE

    fines_dict = yearly_fines.to_dict()
    total_fine = sum(fines_dict.values())
    fines_dict['total'] = total_fine

    fines_output_path = get_data_file_path(data_out_directory, output_filename)

    # TODO: Move to write_json_with_newline once that's merged
    with open(fines_output_path, 'w') as f:
        json.dump(fines_dict, f, indent=2)
        f.write("\n")  # Add EOF newline

    return [ fines_output_path ]

def main():
    # Calculate fines based on non-submission
    calculate_fines()

    # Log completion of this step
    log_step_completion(6, calculate_fines())

if __name__ == "__main__":
    main()
