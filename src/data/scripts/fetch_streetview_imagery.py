"""
Functions to automatically fetch images from the Google Maps API

WIP - not integrated into data pipeline, call from root with with:

```
python3 -m src.data.scripts.fetch_streetview_imagery API_KEY
```

Viktor has a Google Maps API key, or you can create your own!
"""

import os
import sys
import re
import requests
import pandas as pd
from io import BytesIO
from PIL import Image
from typing import List

from src.data.scripts.utils import print_red, print_yellow, print_green


def get_and_store_streetview_image(address: str, api_key: str, size="640x320", fov=80, pitch=10, filename=""):
    """
    Retrieves a Google Street View image for a given address. Returns a filename if an image was
    found and saved, and None otherwise.

    - The max size is 640x640.
    - We use a pitch of 10 (degrees) to angle up a bit for tall buildings and to not show road or
    sidewalk.

    To learn more, see: https://developers.google.com/maps/documentation/streetview/overview
    For full info see: https://developers.google.com/maps/documentation/streetview/request-streetview
    """
    try:
        # Fetch a Streetview image, specifying outdoor (we want photos of, not in, the building)
        # and ensuring we return an error if Google doesn't have imagery, so we don't store a grey
        # placeholder
        url = (
            f"https://maps.googleapis.com/maps/api/streetview?"
            f"source=outdoor&return_error_code=true&"
            f"size={size}&location={address}&"
            f"fov={fov}&pitch={pitch}&"
            f"key={api_key}"
        )
        response = requests.get(url, stream=True)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))

        if filename == "":
            filename = f"{create_img_filename(address)}.webp"

        # Save as a 70% quality webp image to ensure small size
        img.save(filename, optimize=True, quality=70)

        return filename
    except requests.exceptions.RequestException as e:
        # 404 errors mean there's no imagery, so we skip that silently
        if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 404:
            # Do nothing
            print_yellow(f"Google has no imagery for {address}.")
        else:
            # Print other RequestExceptions
            print_red(f"Error fetching Street View image for {address}: {e}")

        return None
    except Exception as e:
        print_red(f"An unexpected error occurred for {address}: {e}")
        return None

def create_img_filename(address: str) -> str:
    """
    Given an address, generates a standardized image filename format. We don't store the city or
    state since this is a Chicago project, but keep the zipcode just in case. Example:

    '10 W 31st Street, Chicago IL, 60616' -> '10_W_31st_St_60616'
    """

    # Remove the city and state parts of the address.
    address_without_city_state = re.sub(r', Chicago IL,?', '', address).strip()

    # Replace spaces with underscores and remove other special characters.
    filename = re.sub(r'[^\w]', '_', address_without_city_state).strip('_')

    return filename

def get_and_store_building_streetview_images(address_list: List[str], api_key: str, output_dir="tmp_streetview_images") -> int:
    """
    Retrieves and saves Google Street View images for a list of addresses. Returns the number of
    images found and stored, since some buildings may not have imagery.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    images_count = 0

    for address in address_list:
        filename = os.path.join(output_dir, f"{create_img_filename(address)}.webp")

        output_filename = get_and_store_streetview_image(address, api_key, filename=filename)

        if output_filename:
            images_count += 1

    return images_count

def load_addresses_from_csv(csv_filepath: str) -> List[str]:
    """
    Read in some addresses from a CSV with an 'address' column, returning an array of addresses
    """

    try:
        df = pd.read_csv(csv_filepath)

        return df['address'].tolist()
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_filepath}' not found.")
        return []

if __name__ == "__main__": # important for command line arguments.
    if len(sys.argv) < 2:
        print("Usage: python script.py <YOUR_API_KEY> [csv_file]")
        sys.exit(1)

    api_key = sys.argv[1]

    if len(sys.argv) > 2:
        csv_file = sys.argv[2]  # Override with command-line argument

    addresses = load_addresses_from_csv(csv_file)

    if len(addresses) > 0:
        print(f"Attempting to fetch imagery for {len(addresses)} buildings...")
        imgs_count = get_and_store_building_streetview_images(addresses, api_key)
        print_green(f"Done, {imgs_count} of {len(addresses)} buildings had images found and stored!")
        print('Make sure to verify imagery looks good before it is published!')
    else:
        print_red('Error! No addresses provided')