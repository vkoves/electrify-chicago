import pandas as pd
from unittest.mock import patch
import json
import tempfile
import os

from src.data.scripts.calculate_fines import calculate_fines, ANNUAL_MAX_FINE


def test_calculate_fines_basic():
    """Test basic fines calculation with mock data."""
    # Create mock historic data
    mock_data = pd.DataFrame(
        {
            "ReportingStatus": [
                "Not Submitted",
                "Not Submitted",
                "Submitted",
                "Not Submitted",
            ],
            "DataYear": [2020, 2020, 2021, 2022],
        }
    )

    with patch(
        "src.data.scripts.calculate_fines.get_and_clean_csv", return_value=mock_data
    ):
        with patch("src.data.scripts.calculate_fines.get_data_file_path") as mock_path:
            with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
                mock_path.return_value = tmp.name

                try:
                    result = calculate_fines()

                    # Check that a file path was returned
                    assert len(result) == 1
                    assert result[0] == tmp.name

                    # Read the written JSON file
                    with open(tmp.name, "r") as f:
                        fines_data = json.load(f)

                    # Check calculations: 2 buildings in 2020, 1 in 2022
                    expected_2020 = 2 * ANNUAL_MAX_FINE
                    expected_2022 = 1 * ANNUAL_MAX_FINE
                    expected_total = expected_2020 + expected_2022

                    assert fines_data["2020"] == expected_2020
                    assert fines_data["2022"] == expected_2022
                    assert fines_data["total"] == expected_total
                    assert (
                        "2021" not in fines_data
                    )  # No non-submitted buildings in 2021

                finally:
                    os.unlink(tmp.name)


def test_calculate_fines_no_violations():
    """Test fines calculation when no buildings violated."""
    mock_data = pd.DataFrame(
        {
            "ReportingStatus": ["Submitted", "Submitted", "Submitted"],
            "DataYear": [2020, 2021, 2022],
        }
    )

    with patch(
        "src.data.scripts.calculate_fines.get_and_clean_csv", return_value=mock_data
    ):
        with patch("src.data.scripts.calculate_fines.get_data_file_path") as mock_path:
            with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
                mock_path.return_value = tmp.name

                try:
                    calculate_fines()

                    with open(tmp.name, "r") as f:
                        fines_data = json.load(f)

                    # Should only have "total": 0
                    assert fines_data["total"] == 0
                    assert len(fines_data) == 1

                finally:
                    os.unlink(tmp.name)


def test_calculate_fines_all_violations():
    """Test fines calculation when all buildings violated."""
    mock_data = pd.DataFrame(
        {
            "ReportingStatus": ["Not Submitted"] * 6,
            "DataYear": [2020, 2020, 2021, 2021, 2021, 2022],
        }
    )

    with patch(
        "src.data.scripts.calculate_fines.get_and_clean_csv", return_value=mock_data
    ):
        with patch("src.data.scripts.calculate_fines.get_data_file_path") as mock_path:
            with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
                mock_path.return_value = tmp.name

                try:
                    calculate_fines()

                    with open(tmp.name, "r") as f:
                        fines_data = json.load(f)

                    # 2 violations in 2020, 3 in 2021, 1 in 2022
                    assert fines_data["2020"] == 2 * ANNUAL_MAX_FINE
                    assert fines_data["2021"] == 3 * ANNUAL_MAX_FINE
                    assert fines_data["2022"] == 1 * ANNUAL_MAX_FINE
                    assert fines_data["total"] == 6 * ANNUAL_MAX_FINE

                finally:
                    os.unlink(tmp.name)
