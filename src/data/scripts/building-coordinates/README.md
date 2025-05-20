# Building Coordinates from Google Maps Platform API

This folder contains a script for pulling an address' coordinates using the
[Google Maps Platform Geocoding API](https://developers.google.com/maps/documentation/geocoding/overview).
We use this information in conjunction with the
[City of Chicago Ward Boundaries](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Wards-2023-Map/cdf7-bgn3)
to identify a building's ward number.

**Building coordinate information is not automatically updated from our data pipeline!** As new buildings
are added to the dataset and ward boundaries as redrawn, these instructions must be manually completed
to generate the source file containing the coordinates (`src/data/source/BuildingCoordinates.xlsx`).

Follow the instructions to generate and save building coordinates for use in the data pipeline.

## Instructions

0. Prerequisite: To run the `./address_geocode.py` script, you must have a Google Maps Platform API Key. See
[Use API Keys with Geocoding API](https://developers.google.com/maps/documentation/geocoding/get-api-key)
for more information.
1. Enter your Google Maps Platform API Key into `./address_geocode.py`.
2. Run `./address_geocode.py`. Due to file pathing limitations, this file must be run from the
electrify-chicago root directory (e.g. `python src/data/scripts/ward-numbers-by-shapes/address_geocode.py`).
3. Wait for the script to generate `src/data/source/BuildingCoordinates.csv`. This may take a few minutes.
4. The source file is now updated for use in the data pipeline!
