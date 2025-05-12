# Geocodes Script

We found multiple errors using the Benchmarking data's provided coordinates and
[Ward boundaries data](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Wards-2023-Map/cdf7-bgn3)
to find ward numbers. After investigation, we found that many of the provided coordinates were inaccurate.
The `./address_geocode.py` script can be manually run to take in addresses from the Benchmarking data and
pull their coordinates from
[Google Maps Platform Geocoding API](https://developers.google.com/maps/documentation/geocoding/overview).
The script saves each building's address and coordinates to `/src/data/source`, which will then be
accessible from the data pipeline.

**This script is not automatically run and integrated into our data pipeline!** The data pipeline
will log whether there are any additional buildings that had been added since the last time this
script had been run.

## Prerequisites

To run the `./address_geocode.py` script, you must have a Google Maps Platform API Key. See
[Use API Keys with Geocoding API](https://developers.google.com/maps/documentation/geocoding/get-api-key)
for more information.
