"""
This module pulls unique addresses from CityEnergyBenchmarking and checks for corresponding Ward
numbers from the City of Chicago Geocoder

City of Chicago Geocoder: https://gisapps.chicago.gov/geocoder/

**Important!** Due to file pathing limitations, this file must be run from the electrify-chicago
root directory (e.g. `python3 src/data/scripts/city-geocodes/unique_addresses.py`)
"""

import pandas as pd


def getUniqueAddresses(benchmarking_data: pd.DataFrame) -> pd.DataFrame:
    unique_addresses = pd.DataFrame(
        benchmarking_data["Address"].dropna().unique(), columns=["Address"]
    )
    return unique_addresses


# Read in energy benchmarking data and only keep unique addresses
building_path = "src/data/source/ChicagoEnergyBenchmarking.csv"
building_benchmarks = pd.read_csv(building_path)
result = getUniqueAddresses(building_benchmarks)

# Save unique addresses
result.to_excel("src/data/scripts/city-geocodes/UniqueAddresses.xlsx", index=False)
