"""
This module processes the City of Chicago Land Inventory to extract information
about city-owned buildings managed by AIS.

It reads data from a CSV export of the Land Inventory, filters for buildings
with the status 'Owned by City' and Managing Organization 'AIS', and then
outputs the processed data in a format suitable for use in
buildings-custom-info.constant.

Data  Source: https://data.cityofchicago.org/Community-Economic-Development/City-Owned-Land-Inventory/aksk-kvfp

**Important!** Due to file pathing limitations, this file must be run from the electrify-chicago
root directory (e.g. `uv run python src/data/scripts/building-owners/find_city_buildings.py`)
"""

import csv
import os

# Input filenames
city_owned_filename = "City-Owned-Land-Inventory.csv"
energy_benchmarking_filepath = "src/data/source/ChicagoEnergyBenchmarking.csv"

found = set()


def clean_address(address):
    return address.lower().strip().replace(" ", "").replace(".", "")


def find_addresses():
    print("Searching for city owned buildings in benchmark data...")
    # Get the directory of the currently executing script
    curr_script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path relative to this script
    city_inventory_path = os.path.join(curr_script_dir, city_owned_filename)

    benchmark_buildings = {}

    # Open the file using the absolute path
    with open(city_inventory_path, "r") as source_file:  # 'r' for reading
        city_file = csv.DictReader(source_file)
        MAIN_FILE_ADDRESS_INDEX = 4
        MAIN_FILE_ID_INDEX = 1

        for i, line in enumerate(city_file):
            if (
                line["Property Status"] == "Owned by City"
                and line["Managing Organization"] == "AIS"
            ):
                benchmark_buildings[clean_address(line["Address"])] = 0

    with open(energy_benchmarking_filepath, newline="") as all_data:
        whole_file = all_data.read().splitlines()

        i = 0  # Initialize i outside the loop
        for i, line in enumerate(whole_file):
            line_arr = line.split(",")

            # Skip broken rows (missing/not enough columns)
            if len(line_arr) > MAIN_FILE_ADDRESS_INDEX:
                address = line_arr[MAIN_FILE_ADDRESS_INDEX]

                if clean_address(address) in benchmark_buildings:
                    found.add(line_arr[MAIN_FILE_ID_INDEX])

            if i % 50 == 49:
                with open("temp.txt", "w") as f:
                    f.write(str(len(found)))
                    f.write("/n")
                    f.write(", ".join(found))

        print(
            f'Found {len(found)} City Owned Addresses in Benchmarking Data Using "{city_owned_filename}"!'
        )
        print(f"\nIDs were: {found.__str__()}")


def print_tags():
    with open("src/data/source/ChicagoEnergyBenchmarking.csv", newline="") as all_data:
        whole_dict = csv.DictReader(all_data)

        print("\nFormatted JS Data (copy into `buildings-custom-info.constant`):\n")
        print("-------")

        for line in whole_dict:
            if line["ID"] in found:
                print("// " + line["Property Name"])
                print(
                    "'"
                    + line["ID"]
                    + "'"
                    + ": { owner: BuildingOwners.cityofchicago.key },"
                )
                found.remove(line["ID"])

        print("------")


# Main
if __name__ == "__main__":
    find_addresses()
    print_tags()
