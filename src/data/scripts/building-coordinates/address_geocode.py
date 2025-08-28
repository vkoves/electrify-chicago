"""
This module processes the addresses in the building benchmarks and extracts coordinates using
the Google Maps Geocoding API

Google Maps Geocoding API: https://developers.google.com/maps/documentation/geocoding/overview

**Important!** Due to file pathing limitations, this file must be run from the electrify-chicago
root directory (e.g. `python3 src/data/scripts/building-owners/find_city_buildings.py`)
"""

import pandas as pd
from typing import Dict

try:
    import googlemaps  # type: ignore

    GOOGLEMAPS_AVAILABLE = True
except ImportError:
    GOOGLEMAPS_AVAILABLE = False
    googlemaps = None  # type: ignore
    print(
        "Warning: googlemaps package not available. Install with 'pip install googlemaps'"
    )

if GOOGLEMAPS_AVAILABLE and googlemaps is not None:
    gmaps = googlemaps.Client(key="YOUR API KEY HERE")
else:
    gmaps = None


def calculateCoordinates(address: str) -> Dict[str, float]:
    """Takes in an address' street number and name in Chicago, IL and returns its coordinates"""
    if not GOOGLEMAPS_AVAILABLE or gmaps is None:
        return {"latitude": 0.0, "longitude": 0.0}

    geocode_result = gmaps.geocode(address + ", Chicago, IL")
    coordinates = geocode_result[0]["geometry"]["location"]
    return {"latitude": coordinates["lat"], "longitude": coordinates["lng"]}


# Read in energy benchmarking data and only keep unique addresses
building_path = "src/data/source/ChicagoEnergyBenchmarking.csv"
building_benchmarks = pd.read_csv(building_path)
unique_addresses = building_benchmarks["Address"].dropna().unique()
building_geocodes = pd.DataFrame({"Address": unique_addresses})

# Fetch and save geocode information for all unique addresses
building_geocodes["Coordinates"] = building_geocodes.apply(
    lambda building: calculateCoordinates(building["Address"]), axis=1
)
building_geocodes.to_csv(
    "src/data/source/BuildingCoordinates.csv", sep=",", encoding="utf-8", index=False
)
