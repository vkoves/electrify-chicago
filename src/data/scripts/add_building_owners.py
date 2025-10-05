"""
Add building owner information to the building data CSV.

Reads the JSON owner mappings file and adds an Owner column to the building data.
This allows GraphQL to filter buildings by owner at query time rather than doing
client-side filtering.
"""

import json
from typing import Dict
from src.data.scripts.utils import (
    get_and_clean_csv,
    get_data_file_path,
    log_step_completion,
    output_to_csv,
)

# Debug flag for development
debug = False

# Input/output paths
data_out_directory = "dist"
building_emissions_file = "building-benchmarks.csv"
owners_json_path = "src/constants/building-owners-mapping.json"


def parse_owner_mappings(json_file: str) -> Dict[str, str]:
    """
    Load building owner mappings from JSON file.

    Returns a dictionary mapping building ID (string) to owner key (string).
    Example: {'251330': 'depaul', '101920': 'cityofchicago'}
    """
    owner_map = {}

    with open(json_file, "r", encoding="utf-8") as f:
        owners_data = json.load(f)

    # Convert from {owner: [building_ids]} to {building_id: owner}
    for owner_key, building_ids in owners_data.items():
        for building_id in building_ids:
            owner_map[str(building_id)] = owner_key

    if debug:
        print(f"Loaded {len(owner_map)} owner mappings from {json_file}")
        # Show some examples
        for bid, owner in list(owner_map.items())[:5]:
            print(f"  Building {bid} -> {owner}")

    return owner_map


def add_owners_to_buildings() -> str:
    """
    Add Owner column to building data CSV based on owner mappings.

    Returns the output file path.
    """
    # Load owner mappings from JSON file
    owner_map = parse_owner_mappings(owners_json_path)

    # Read the final building data CSV (after process_data.py)
    building_data = get_and_clean_csv(
        get_data_file_path(data_out_directory, building_emissions_file)
    )

    # Add Owner column - map building ID to owner key
    building_data["Owner"] = (
        building_data["ID"].astype(str).map(lambda x: owner_map.get(x))
    )

    if debug:
        matched_count = building_data["Owner"].notna().sum()
        print(
            f"Added owner info to {matched_count} of {len(building_data)} building records"
        )

    # Write back to the final CSV
    output_path = get_data_file_path(data_out_directory, building_emissions_file)
    output_to_csv(building_data, output_path)

    return output_path


def main() -> None:
    output_path = add_owners_to_buildings()
    log_step_completion(3, [output_path])


if __name__ == "__main__":
    main()
