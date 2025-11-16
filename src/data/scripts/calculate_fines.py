"""
A script that calculates an estimated amount of fines the city could have collected during each year of reporting, under
the assumption the buildings that didn't comply would have not complied that whole year.

The fines by year (along with # of buildings not in compliance) and grand totals get written to
fines-by-year.json

**Important!** Due to file pathing, this file must be run from the project root, via:

```
uv run python -m src.data.scripts.calculate_fines
```
"""

from src.data.scripts.utils import (
    get_and_clean_csv,
    get_data_file_path,
    log_step_completion,
    write_json_with_newline,
)

# THe maximum fine a building would get from not complying in a year, from the official ordinance
ANNUAL_MAX_FINE = 9200

# We use the historic data (benchmarking all years) to get years that were and were not submitted
historic_data_in_filename = "benchmarking-all-years.csv"

output_filename = "fines-by-year.json"

# Assume run in /data
data_out_directory = "dist"


def calculate_fines() -> list[str]:
    """
    Calculates fines that could have been collected

    Returns an array of files written to
    """

    # Read the built historic data
    historic_data = get_and_clean_csv(
        get_data_file_path(data_out_directory, historic_data_in_filename)
    )

    not_submitted = historic_data[historic_data["ReportingStatus"] == "Not Submitted"]

    yearly_counts_ser = not_submitted.groupby("DataYear").size()

    # Built up a dictionary, e.g.
    # {
    #   2018: { fines: 9_200_000, count: 1_000 },
    #   total: { fines: ..., count: ... }
    # }
    fines_dict = {}

    for year, count in yearly_counts_ser.items():
        # Calculate fines using the single 'count' integer value
        fines = count * ANNUAL_MAX_FINE

        # Populate the dictionary for the year. .item() converts
        # the pandas integer to a standard Python integer, ensuring
        # maximum JSON compatibility, although often unnecessary.
        fines_dict[str(year)] = {
            'fines': fines,
            'count': count
        }

    total_count = int(yearly_counts_ser.sum())

    fines_dict["total"] = { 'count': total_count, 'fines': total_count * ANNUAL_MAX_FINE }

    fines_output_path = get_data_file_path(data_out_directory, output_filename)

    write_json_with_newline(fines_dict, fines_output_path, indent=2)

    return [fines_output_path]


def main():
    # Calculate fines based on non-submission
    calculate_fines()

    # Log completion of this step
    log_step_completion(6, calculate_fines())


if __name__ == "__main__":
    main()
