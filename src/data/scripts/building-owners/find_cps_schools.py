"""
Find CPS (Chicago Public Schools) properties by searching specifically for the term "CPS" in the
property name.

NOTE: This does not include ALL buildings, so we manually tagged selective enrollment schools

This script will then log the correctly formatted data, and you can copy that into
buildings-custom-info.constant

**Important!** Due to file pathing limitations, this file must be run from the electrify-chicago
root directory (e.g. `uv run python src/data/scripts/building-owners/find_cps_buildings.py`)
"""

import csv

energy_benchmarking_filepath = 'src/data/source/ChicagoEnergyBenchmarking.csv'

cps_schools:[str, str] = {}

with open(energy_benchmarking_filepath, newline='') as csvfile:
    whole_file = csv.DictReader(csvfile)

    for row in whole_file:
        if "CPS" in row["Property Name"]:
            cps_schools[row["ID"]] = row["Property Name"]

    print(f"Found {len(cps_schools)} CPS Addresses in Benchmarking Data Using search for 'CPS' in Property Name!")

    print("\nFormatted JS Data (copy into `buildings-custom-info.constant`):\n")
    print("-------")

    for id, school in cps_schools.items():
        cleaned_school_name = school.removesuffix("-CPS").strip()

        print("// " + cleaned_school_name)
        print('"' + id + '"' + ": { owner: BuildingOwners.cps.key },")
