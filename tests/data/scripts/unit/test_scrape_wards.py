"""Tests for the ward information scraper."""

import csv
import tempfile
import os
from unittest.mock import patch, MagicMock

from src.data.scripts.scrape_wards import (
    extract_ward_info,
    fetch_page,
    KEYWORD_ALDERMAN,
    KEYWORD_WARD_OFFICE,
    KEYWORD_EMAIL,
    KEYWORD_PHONE,
    KEYWORD_FAX,
    KEYWORD_CITY_HALL,
    DEFAULT_CITY,
    DEFAULT_STATE,
    DEFAULT_CITY_HALL_ADDRESS,
)


# Sample HTML content mimicking Chicago city website structure
SAMPLE_HTML_WARD_1 = """
<!DOCTYPE html>
<html>
<head><title>Ward 1</title></head>
<body>
<div class="page-description">
<h3>Alderman Daniel La Spata</h3>

<p><strong>Ward Office:</strong><br>
1958 N. Milwaukee Ave.<br>
Chicago, IL 60647</p>

<p><strong>Email:</strong><br>
<a href="mailto:info@the1stward.com">info@the1stward.com</a></p>

<p><strong>Phone:</strong><br>
872.206.2685</p>

<p><strong>Fax:</strong><br>
312.448.8829</p>

<p><strong>City Hall Office:</strong><br>
121 N. La Salle<br>
Room 200<br>
Chicago, IL 60602</p>
</div>
</body>
</html>
"""

# HTML with multi-word last name
SAMPLE_HTML_WARD_40 = """
<!DOCTYPE html>
<html>
<head><title>Ward 40</title></head>
<body>
<div class="page-description">
<h3>Alderman Andre Vasquez, Jr.</h3>

<p><strong>Ward Office:</strong><br>
5620 N. Western Ave.<br>
Chicago, IL 60659</p>

<p><strong>Email:</strong><br>
<a href="mailto:info@40thward.org">info@40thward.org</a></p>

<p><strong>Phone:</strong><br>
773.654.1867</p>

<p><strong>City Hall Office:</strong><br>
121 N. La Salle<br>
Room 300<br>
Chicago, IL 60602</p>
</div>
</body>
</html>
"""

# HTML with minimal information
SAMPLE_HTML_MINIMAL = """
<!DOCTYPE html>
<html>
<head><title>Ward 99</title></head>
<body>
<div class="page-description">
<h3>Alderman Test Person</h3>

<p><strong>Email:</strong><br>
<a href="mailto:ward99@cityofchicago.org">ward99@cityofchicago.org</a></p>

<p><strong>Phone:</strong><br>
312.555.1234</p>
</div>
</body>
</html>
"""


def test_extract_ward_info_basic():
    """Test basic ward information extraction."""
    ward_info = extract_ward_info(SAMPLE_HTML_WARD_1, 1, debug=False)

    assert ward_info["Name"] == "Daniel La Spata"
    assert ward_info["Office"] == 1
    assert ward_info["Email"] == "info@the1stward.com"
    assert ward_info["Office Phone"] == "(872) 206-2685"
    assert ward_info["Fax"] == "(312) 448-8829"
    assert ward_info["Office Address"] == "1958 N. Milwaukee Ave."
    assert ward_info["City"] == "Chicago"
    assert ward_info["State"] == "IL"
    assert ward_info["Zip"] == "60647"
    assert ward_info["City Hall City"] == DEFAULT_CITY
    assert ward_info["City Hall State"] == DEFAULT_STATE


def test_extract_ward_info_multiword_name():
    """Test extraction with multi-word last name (Vasquez, Jr.)."""
    ward_info = extract_ward_info(SAMPLE_HTML_WARD_40, 40, debug=False)

    assert ward_info["Name"] == "Andre Vasquez, Jr."
    assert ward_info["Office"] == 40
    assert ward_info["Email"] == "info@40thward.org"
    assert ward_info["Office Phone"] == "(773) 654-1867"
    assert ward_info["Office Address"] == "5620 N. Western Ave."
    assert ward_info["Zip"] == "60659"


def test_extract_ward_info_minimal():
    """Test extraction with minimal information available."""
    ward_info = extract_ward_info(SAMPLE_HTML_MINIMAL, 99, debug=False)

    assert ward_info["Name"] == "Test Person"
    assert ward_info["Office"] == 99
    assert ward_info["Email"] == "ward99@cityofchicago.org"
    assert ward_info["Office Phone"] == "(312) 555-1234"
    assert ward_info["Fax"] == ""
    assert ward_info["Office Address"] == ""
    # Should use defaults when info is missing
    assert ward_info["City"] == DEFAULT_CITY
    assert ward_info["State"] == DEFAULT_STATE


def test_extract_ward_info_no_fax():
    """Test that fax is optional."""
    ward_info = extract_ward_info(SAMPLE_HTML_WARD_40, 40, debug=False)
    assert ward_info["Fax"] == ""


def test_extract_ward_info_preserves_special_chars():
    """Test that special characters in names are preserved."""
    ward_info = extract_ward_info(SAMPLE_HTML_WARD_40, 40, debug=False)
    # Should preserve comma and period in "Vasquez, Jr."
    assert "," in ward_info["Name"]
    assert "." in ward_info["Name"]


def test_constants_are_used():
    """Test that keyword constants are properly defined."""
    # Verify that all required constants exist
    assert KEYWORD_ALDERMAN == "Alderman"
    assert KEYWORD_WARD_OFFICE == "Ward Office"
    assert KEYWORD_EMAIL == "Email"
    assert KEYWORD_PHONE == "Phone"
    assert KEYWORD_FAX == "Fax"
    assert KEYWORD_CITY_HALL == "City Hall Office"


def test_fetch_page_uses_correct_url():
    """Test that fetch_page constructs the correct URL."""
    with patch("src.data.scripts.scrape_wards.urlopen") as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = b"<html></html>"
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        fetch_page(1)

        # Check that urlopen was called
        assert mock_urlopen.called
        # Check that the URL includes ward 01
        call_args = mock_urlopen.call_args[0][0]
        assert "wards/01.html" in call_args.full_url


def test_fetch_page_handles_errors():
    """Test that fetch_page handles network errors gracefully."""
    with patch("src.data.scripts.scrape_wards.urlopen") as mock_urlopen:
        mock_urlopen.side_effect = Exception("Network error")

        result = fetch_page(1)

        assert result is None


def test_csv_output_format():
    """Test that CSV output has the correct structure."""
    from src.data.scripts.scrape_wards import main

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp:
        output_file = tmp.name

    try:
        # Mock the entire scraping process
        with patch("src.data.scripts.scrape_wards.OUTPUT_FILE", output_file):
            with patch("src.data.scripts.scrape_wards.fetch_page") as mock_fetch:
                mock_fetch.return_value = SAMPLE_HTML_WARD_1

                # Run for just ward 1
                main(test_ward=1, debug=False)

        # Read and verify the CSV
        with open(output_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

            # Check CSV structure
            assert len(rows) == 1
            row = rows[0]

            # Verify all expected columns are present
            expected_columns = [
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
            for col in expected_columns:
                assert col in row

            # Verify content
            assert row["Name"] == "Daniel La Spata"
            assert row["Office"] == "1"

    finally:
        if os.path.exists(output_file):
            os.unlink(output_file)


def test_phone_number_formatting():
    """Test that phone numbers are properly formatted."""
    ward_info = extract_ward_info(SAMPLE_HTML_WARD_1, 1, debug=False)

    # Should be formatted as (XXX) XXX-XXXX
    phone = ward_info["Office Phone"]
    assert phone.startswith("(")
    assert ") " in phone
    assert "-" in phone
    assert len(phone) == 14  # (XXX) XXX-XXXX format


def test_default_city_hall_address():
    """Test that default City Hall address is used when not found."""
    ward_info = extract_ward_info(SAMPLE_HTML_MINIMAL, 99, debug=False)
    assert ward_info["City Hall Address"] == DEFAULT_CITY_HALL_ADDRESS
