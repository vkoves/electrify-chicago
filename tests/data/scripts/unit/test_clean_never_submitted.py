import pandas as pd
import pytest

from src.data.scripts import clean_and_split_data
from tests.data.scripts.utils import get_test_file_path

test_input_file = "test_never_submitted_src_data.csv"


@pytest.fixture
def processed_dataframe() -> pd.DataFrame:
    """Process our never-submitted test data as per clean_and_split_data.py, passing True for
    latest_year_only, and return the resulting dataframe"""

    input_filename = get_test_file_path(test_input_file)
    df = clean_and_split_data.process(input_filename, True)

    assert df is not None
    return df


def test_never_submitted_building_is_included(processed_dataframe):
    """Building 500002 has "Not Submitted" status in every year on record, so it should still get
    a single row in the output (rather than being dropped entirely), using its most recent year"""

    df = processed_dataframe
    building_rows = df[df["ID"] == 500002]

    assert len(building_rows) == 1
    assert building_rows.iloc[0]["DataYear"] == 2023
    assert building_rows.iloc[0]["ReportingStatus"] == "Not Submitted"
    assert pd.isna(building_rows.iloc[0]["GHGIntensity"])


def test_previously_submitted_building_uses_last_submitted_year(processed_dataframe):
    """Building 500003 submitted in 2021 but not in 2023 - it should still use its last
    *submitted* year (2021), not the never-submitted logic added for building 500002"""

    df = processed_dataframe
    building_rows = df[df["ID"] == 500003]

    assert len(building_rows) == 1
    assert building_rows.iloc[0]["DataYear"] == 2021
    assert building_rows.iloc[0]["ReportingStatus"] == "Submitted"
    assert building_rows.iloc[0]["GHGIntensity"] > 0


def test_property_count_includes_never_submitted(processed_dataframe):
    """Confirm we get exactly one row per building, including the never-submitted one"""

    df = processed_dataframe
    assert len(df) == 3


def test_get_never_submitted_buildings_excludes_ever_submitted():
    """Unit test for get_never_submitted_buildings directly: a building with a submitted row in
    any year should never show up, even if that row isn't the most recent one"""

    building_data = pd.DataFrame(
        [
            {"ID": "1", "DataYear": 2022, "ReportingStatus": "Not Submitted"},
            {"ID": "1", "DataYear": 2023, "ReportingStatus": "Not Submitted"},
            {"ID": "2", "DataYear": 2021, "ReportingStatus": "Submitted"},
            {"ID": "2", "DataYear": 2023, "ReportingStatus": "Not Submitted"},
        ]
    )

    result = clean_and_split_data.get_never_submitted_buildings(building_data)

    assert list(result["ID"]) == ["1"]
    assert result.iloc[0]["DataYear"] == 2023
