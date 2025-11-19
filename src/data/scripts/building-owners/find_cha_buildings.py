"""
Reads from cha_building_names, which is sourced from:
https://www.thecha.org/residents/public-housing/find-public-housing

This script will then log the correctly formatted data, and you can copy that into
buildings-custom-info.constant

**Important!** Due to file pathing limitations, this file must be run from the electrify-chicago
root directory (e.g. `uv run python src/data/scripts/building-owners/find_cha_buildings.py`)
"""

import csv

found = []

cha_buildings_filename = "src/data/scripts/building-owners/cha_building_names.txt"
energy_benchmarking_filepath = "src/data/source/ChicagoEnergyBenchmarking.csv"

with open(cha_buildings_filename) as f:
    looking_for = f.read().splitlines()

    with open(energy_benchmarking_filepath) as a:
        whole_file = list(csv.DictReader(a))

        for i, p in enumerate(looking_for):
            for j, whole_file_line in enumerate(whole_file):
                if p.lower().strip().replace(" ", "") in whole_file_line[
                    "Property Name"
                ].lower().strip().replace(" ", ""):
                    found.append(
                        (whole_file_line["ID"], whole_file_line["Property Name"])
                    )
                    break


print(
    f'Found {len(found)} CHA Addresses in Benchmarking Data Using "{cha_buildings_filename}"!'
)

print("\nFormatted JS Data (copy into `buildings-custom-info.constant`):\n")
print("-------")

for place in found:
    print("// " + place[1])
    print("'" + place[0] + "'" + ": { owner: BuildingOwners.cha.key },")

print("-------")
