# City Geocodes by Addresses

The [City of Chicago Geocoder](https://gisapps.chicago.gov/geocoder/) provides city geocode information
by address. We use this information to identify a building's ward number.

**City geocode information is not automatically updated from our data pipeline!** As new buildings
are added to the dataset and ward boundaries as redrawn, these instructions must be manually completed
to generate a source file containing the city geocode information.

Follow the instructions to update the source file: `src/data/source/CityGeocoder.xlsx`.

## Instructions

1. Run `./unique_addresses.py`. Due to file pathing limitations, this file must be run from the
   electrify-chicago root directory (e.g. `python src/data/scripts/ward-numbers/unique_addresses.py`). This
   script generates `./UniqueAddresses.xlsx`.
2. Navigate to the
   [City of Chicago Geocoder - Bulk Geocode](https://gisapps.chicago.gov/geocoder/bulkgeo/single). Upload
   `./UniqueAddresses.xlsx`.
3. Select: 1st Row Contains Column Names? > Yes, then click "Next >"
4. Select: Column > Address, then click "Next >"
5. Select: Selected Geographies > Wards (Current - 2023), then click "Submit"
6. Wait for the results to finish processing (may take a few minutes)
7. Download results. Rename `bulkgeo-results.xlsx` to `CityGeocoder.xlsx` and save to `src/data/source/`.
8. The source file is now updated for use in the data pipeline!
