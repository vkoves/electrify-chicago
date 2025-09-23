"""
Utils - Basic utilities for file processing that are agnostic to the specific
data being processed
"""

import pandas as pd
import pathlib

from typing import List

# ANSI color codes for output
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
LIGHT_BLUE = "\033[0;34m"
NC = "\033[0m"  # No Color


def print_red(msg: str) -> None:
    """Print to the console with red text"""
    print(f"{RED}{msg}{NC}")


def print_yellow(msg: str) -> None:
    """Print to the console with yellow text"""
    print(f"{YELLOW}{msg}{NC}")


def print_green(msg: str) -> None:
    """Print to the console with green text"""
    print(f"{GREEN}{msg}{NC}")


def get_data_file_path(dir: str, f: str) -> str:
    """Get path for source data file to process (in src/data)"""

    curr_path = pathlib.Path(".")
    path = curr_path.parent.absolute() / "src" / "data" / dir / f

    return str(path)


def get_and_clean_csv(path_to_csv, cols_to_keep=None) -> pd.DataFrame:
    """Fetch a building benchmarking CSV in Pandas, keeping the cols_to_keep (if specified)"""

    # Create a dictionary mapping column names (or indices) to dtypes:
    data_types = {
        # Specify that "Exempt From Chicago Energy Rating" column is a string, preventing default
        # boolean parsing and warning of mixed types
        7: "string",
    }

    df = pd.read_csv(path_to_csv, dtype=data_types)  # type: ignore

    if cols_to_keep is None:
        return df
    else:
        return df[cols_to_keep]


def output_to_csv(building_data: pd.DataFrame, output_path: str) -> None:
    """Output a Pandas dataframe to a CSV file"""
    building_data.to_csv(output_path, sep=",", encoding="utf-8", index=False)


def json_data_builder(
    dataframe, outer_tag="default", is_array=True, array_key="emissionsByYear"
) -> List[str]:
    """Process the a CSV dataframe into a JSON object"""

    uniqueColKey = "ID"

    dataframe = dataframe.map(lambda x: "" if pd.isnull(x) else x)

    # initiate empty json object to iterate with
    json_object = []

    # grab list of unique states for for_loop
    unique_buildings = list(set(dataframe[uniqueColKey]))

    for building in unique_buildings:
        building_df = dataframe.loc[dataframe[uniqueColKey] == building]
        # # need to set building as the index here, so it's not duplicated in our final json
        # if is_array:
        #     building_df.set_index(uniqueColKey, inplace=True)
        #     building_json = building_df.to_dict('records')
        #     json_object.append({"building": building, array_key: building_json})
        # else:
        building_json = building_df.to_dict("records")[0]
        json_object.append(building_json)

    # Return outer tag output object
    return json_object


def log_step_completion(step_num, outputted_paths):
    """Logs the completion of a data processing step and the paths of exported files.

    This function prints a message indicating the completion of a specific step
    in our data processing pipeline, along with a list of the files that were
    exported during that step. Debug files (in /debug) are printed first with a
    "(debug)" note for clarity.

    Args:
        step_num (int): The number of the completed step (e.g., 1, 2, 3).
        outputted_paths (list): A list of file paths (strings or Path objects)
            that were outputted by the step.  May contain None values which are ignored.

    Returns:
        None
    """

    debug_paths = []
    other_paths = []

    for path in outputted_paths:
        if path:
            path_str = str(path)  # Convert to string for easier manipulation
            if "/debug" in path_str:
                debug_paths.append(path_str)
            else:
                other_paths.append(path_str)

    print(f"Step {step_num} data processing done! Files exported/updated:\n")

    for path in debug_paths:
        print(f" - {YELLOW}{path} (debug){NC}")  # Yellow text for debug paths

    for path in other_paths:
        print(f" - {path}")
