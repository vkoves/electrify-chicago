#!/usr/bin/env python3
"""
Scrapes alderperson contact information from the official Chicago city website.

The city's ward pages (https://www.chicago.gov/city/en/about/wards/) contain more accurate and
up-to-date alderperson contact information than other sources. This script fetches and parses
contact details for all 50 wards.

Output file: dist/alders-info.csv (also accessible via symlink at static/alders-info.csv)

Columns in output:
- Name: Alderperson's full name
- Office: Ward number (1-50)
- Office Phone: Ward office phone number
- Fax: Ward office fax number (if available)
- Email: Ward office email address
- Website: Ward website URL
- Office Address: Street address of ward office
- City, State, Zip: Ward office location details
- City Hall Phone: Phone at City Hall office
- City Hall Address: City Hall office location
- City Hall City, City Hall State, City Hall Zip: City Hall location details

Usage:
    # Scrape all 50 wards (takes ~30 seconds)
    python3 src/data/scripts/scrape_wards.py

    # Test with ward 1 only (with debug output)
    python3 src/data/scripts/scrape_wards.py --test

    # Scrape specific wards
    python3 src/data/scripts/scrape_wards.py --wards 11,21,40,48
"""

import csv
import re
import time
import os
from urllib.request import urlopen, Request
from html.parser import HTMLParser


# Configuration constants - Update these if city website structure changes
WARD_URL_TEMPLATE = "https://www.chicago.gov/city/en/about/wards/{ward_num:02d}.html"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"

# Output file path - goes to dist/ and is symlinked from static/
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(_SCRIPT_DIR, "..", "dist", "alders-info.csv")

# Parsing keywords - Update these if website text changes
KEYWORD_ALDERMAN = "Alderman"
KEYWORD_WARD_OFFICE = "Ward Office"
KEYWORD_EMAIL = "Email"
KEYWORD_PHONE = "Phone"
KEYWORD_FAX = "Fax"
KEYWORD_CITY_HALL = "City Hall Office"

# Default values
DEFAULT_CITY = "Chicago"
DEFAULT_STATE = "IL"
DEFAULT_CITY_HALL_ADDRESS = "121 North LaSalle Street, Room 200"
DEFAULT_CITY_HALL_ZIP = "60602"

# Script settings
REQUEST_TIMEOUT = 10  # seconds
REQUEST_DELAY = 0.5  # seconds between requests


class SimpleHTMLParser(HTMLParser):
    """Simple HTML parser to extract text content."""

    def __init__(self):
        super().__init__()
        self.text_content = []
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag

    def handle_data(self, data):
        text = data.strip()
        if text:
            self.text_content.append(text)

    def get_text(self):
        return " ".join(self.text_content)


def fetch_page(ward_num):
    """Fetch a ward page from Chicago city website."""
    url = WARD_URL_TEMPLATE.format(ward_num=ward_num)
    headers = {"User-Agent": USER_AGENT}

    try:
        request = Request(url, headers=headers)
        with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            html = response.read().decode("utf-8")
            return html
    except Exception as e:
        print(f"Error fetching ward {ward_num}: {e}")
        return None


def extract_ward_info(html, ward_num, debug=False):
    """Extract contact information from ward page HTML."""
    parser = SimpleHTMLParser()
    parser.feed(html)
    content = parser.get_text()

    # Extract alderman name from h3 tag pattern
    # More flexible pattern that captures the name until we hit contact info keywords
    keywords_pattern = f"(?:\\s+{KEYWORD_WARD_OFFICE}|\\s+{KEYWORD_EMAIL}|\\s+{KEYWORD_PHONE}|\\s+{KEYWORD_CITY_HALL}|$)"
    name_match = re.search(
        rf"{KEYWORD_ALDERMAN}\s+([A-Za-z][A-Za-z\s\.,\'-]+?){keywords_pattern}",
        content,
        re.IGNORECASE,
    )
    if not name_match:
        # Try alternative pattern for cases where "Alderman" appears alone
        name_match = re.search(
            rf"{KEYWORD_ALDERMAN}\s+([A-Za-z][A-Za-z\s\.,\'-]{{2,50}})",
            content,
            re.IGNORECASE,
        )

    name = ""
    if name_match:
        name = name_match.group(1).strip()
        # Clean up any trailing text that might have been captured
        name = re.sub(r"\s+(Ward\s+)?Office.*$", "", name, flags=re.IGNORECASE).strip()
        cleanup_keywords = (
            f"({KEYWORD_EMAIL}|{KEYWORD_PHONE}|{KEYWORD_CITY_HALL}|{KEYWORD_FAX})"
        )
        name = re.sub(
            rf"\s+{cleanup_keywords}.*$", "", name, flags=re.IGNORECASE
        ).strip()

    if debug:
        print(f"Name extracted: '{name}'")

    # Extract email
    email_match = re.search(
        rf"{KEYWORD_EMAIL}[:\s]+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{{2,}})",
        content,
        re.IGNORECASE,
    )
    email = email_match.group(1) if email_match else ""
    if debug:
        print(f"Email extracted: '{email}'")

    # Extract phone
    phone_lookahead = (
        f"(?=\\s*{KEYWORD_FAX}|\\s*{KEYWORD_CITY_HALL}|\\s*{KEYWORD_EMAIL}|$)"
    )
    phone_match = re.search(
        rf"{KEYWORD_PHONE}[:\s]+([\d\.\-\(\)\s]+?){phone_lookahead}",
        content,
        re.IGNORECASE,
    )
    office_phone = ""
    if phone_match:
        phone_raw = phone_match.group(1).strip()
        # Clean up phone number
        digits = re.findall(r"\d+", phone_raw)
        if digits:
            phone_str = "".join(digits)
            if len(phone_str) >= 10:
                office_phone = f"({phone_str[:3]}) {phone_str[3:6]}-{phone_str[6:10]}"
    if debug:
        print(f"Phone extracted: '{office_phone}'")

    # Extract fax
    fax_lookahead = (
        f"(?=\\s*{KEYWORD_CITY_HALL}|\\s*{KEYWORD_EMAIL}|\\s*{KEYWORD_WARD_OFFICE}|$)"
    )
    fax_match = re.search(
        rf"{KEYWORD_FAX}[:\s]+([\d\.\-\(\)\s]+?){fax_lookahead}", content, re.IGNORECASE
    )
    fax = ""
    if fax_match:
        fax_raw = fax_match.group(1).strip()
        # Clean up fax number
        digits = re.findall(r"\d+", fax_raw)
        if digits:
            fax_str = "".join(digits)
            if len(fax_str) >= 10:
                fax = f"({fax_str[:3]}) {fax_str[3:6]}-{fax_str[6:10]}"
    if debug:
        print(f"Fax extracted: '{fax}'")

    # Extract ward office address
    ward_office_match = re.search(
        rf"{KEYWORD_WARD_OFFICE}[:\s]+([0-9]+[^\n]+?)\s+([A-Za-z\s]+),?\s*([A-Z]{{2}})\s*(\d{{5}})",
        content,
        re.IGNORECASE,
    )

    office_address = ""
    city = DEFAULT_CITY
    state = DEFAULT_STATE
    zip_code = ""

    if ward_office_match:
        office_address = ward_office_match.group(1).strip().rstrip(",")
        city = ward_office_match.group(2).strip()
        state = ward_office_match.group(3).strip()
        zip_code = ward_office_match.group(4).strip()

    if debug:
        print(
            f"Office Address extracted: '{office_address}, {city}, {state} {zip_code}'"
        )

    # Extract City Hall office address
    city_hall_match = re.search(
        rf"{KEYWORD_CITY_HALL}[:\s]+([0-9]+[^\n]+?(?:Room[^\n]+?)?)\s+[A-Za-z\s]+,?\s*[A-Z]{{2}}\s*\d{{5}}",
        content,
        re.IGNORECASE,
    )
    city_hall_address = DEFAULT_CITY_HALL_ADDRESS
    if city_hall_match:
        city_hall_address = city_hall_match.group(1).strip().rstrip(",")

    if debug:
        print(f"City Hall Address extracted: '{city_hall_address}'")

    # Website - check if there's an actual website mentioned
    website = ""
    # Look for common ward website patterns in the HTML
    website_match = re.search(r'(https?://[^\s<>"]+ward[^\s<>"]*)', html, re.IGNORECASE)
    if website_match:
        website = website_match.group(1).rstrip("/")

    if debug:
        print(f"Website extracted: '{website}'")
        print("--- End Debug ---\n")

    return {
        "Name": name,
        "Office": ward_num,
        "Office Phone": office_phone,
        "Fax": fax,
        "Email": email,
        "Website": website,
        "Office Address": office_address,
        "City": city,
        "State": state,
        "Zip": zip_code,
        "City Hall Phone": office_phone,  # Often same as office phone
        "City Hall Address": city_hall_address,
        "City Hall City": DEFAULT_CITY,
        "City Hall State": DEFAULT_STATE,
        "City Hall Zip": DEFAULT_CITY_HALL_ZIP,
    }


def main(test_ward=None, debug=False):
    """Main function to scrape all wards and save to CSV.

    Args:
        test_ward: If specified, only scrape this ward number (for testing)
        debug: If True, print detailed debug information
    """
    print("Starting ward information scraper...")

    all_wards = []

    # Determine which wards to scrape
    if test_ward:
        ward_range = [test_ward]
        print(f"TEST MODE: Only scraping ward {test_ward}")
    else:
        ward_range = range(1, 51)

    for ward_num in ward_range:
        print(f"\nFetching ward {ward_num}...")

        html = fetch_page(ward_num)
        if html:
            ward_info = extract_ward_info(html, ward_num, debug=debug)
            all_wards.append(ward_info)
            print(f"  ✓ Ward {ward_num}: {ward_info['Name']}")
            print(f"     Email: {ward_info['Email']}")
            print(f"     Phone: {ward_info['Office Phone']}")
            print(f"     Address: {ward_info['Office Address']}")
        else:
            print(f"  ✗ Ward {ward_num}: Failed to fetch")

        # Be nice to the server
        if not test_ward:
            time.sleep(REQUEST_DELAY)

    # Write to CSV
    output_file = OUTPUT_FILE

    fieldnames = [
        "Name",
        "Office",
        "Office Phone",
        "Fax",
        "Email",
        "Website",
        "Office Address",
        "City",
        "State",
        "Zip",
        "City Hall Phone",
        "City Hall Address",
        "City Hall City",
        "City Hall State",
        "City Hall Zip",
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_wards)

    print(f"\n✓ Successfully scraped {len(all_wards)} ward(s)")
    print(f"✓ Data saved to {output_file}")


if __name__ == "__main__":
    import sys

    # Check for arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            main(test_ward=1, debug=True)
        elif sys.argv[1] == "--wards":
            # Allow specifying specific wards: --wards 11,21,40,48
            if len(sys.argv) > 2:
                ward_nums = [int(w.strip()) for w in sys.argv[2].split(",")]
                for ward_num in ward_nums:
                    main(test_ward=ward_num, debug=True)
            else:
                print("Usage: --wards 11,21,40,48")
        else:
            print("Usage: scrape_wards.py [--test] [--wards ward1,ward2,...]")
    else:
        main()
