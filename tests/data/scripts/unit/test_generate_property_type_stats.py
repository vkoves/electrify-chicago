import pytest
import pandas as pd
from unittest.mock import patch, mock_open
from src.data.scripts.generate_property_type_stats import (
    calculate_building_stats,
    rank_buildings_by_property_type,
    building_cols_to_rank,
)


@pytest.fixture
def sample_building_data():
    """Create sample building data with two property types for testing"""
    data = {
        "PrimaryPropertyType": ["Office", "Office", "Office", "Hotel", "Hotel"],
        "GHGIntensity": [5.0, 7.0, 9.0, 10.0, 12.0],
        "TotalGHGEmissions": [1000.0, 2000.0, 3000.0, 1500.0, 2500.0],
        "ElectricityUse": [500000.0, 1000000.0, 1500000.0, 800000.0, 1200000.0],
        "NaturalGasUse": [300000.0, 600000.0, 900000.0, 400000.0, 700000.0],
        "GrossFloorArea": [50000.0, 100000.0, 150000.0, 75000.0, 125000.0],
        "SourceEUI": [100.0, 120.0, 140.0, 150.0, 170.0],
        "SiteEUI": [60.0, 75.0, 90.0, 80.0, 100.0],
        "AvgPercentileLetterGrade": ["A", "B", "C", "B", "C"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def grouped_by_prop_type(sample_building_data):
    return sample_building_data.groupby("PrimaryPropertyType")


@pytest.fixture
def property_types(grouped_by_prop_type):
    return [str(key) for key in grouped_by_prop_type.groups.keys()]


def test_calculate_building_stats_returns_file_path(
    property_types, grouped_by_prop_type
):
    """Test that calculate_building_stats returns the expected file path"""
    with (
        patch(
            "src.data.scripts.generate_property_type_stats.property_stats_file_path",
            "/mock/stats/path",
        ),
        patch("builtins.open", mock_open()),
        patch("json.dump"),
    ):
        result = calculate_building_stats(property_types, grouped_by_prop_type)
        assert result == "/mock/stats/path"


def test_calculate_building_stats_data_structure(property_types, grouped_by_prop_type):
    """Test that output contains expected property types and stat keys"""
    with (
        patch(
            "src.data.scripts.generate_property_type_stats.property_stats_file_path",
            "/mock/stats/path",
        ),
        patch("builtins.open", mock_open()),
        patch("json.dump") as mock_json_dump,
    ):
        calculate_building_stats(property_types, grouped_by_prop_type)

        stats = mock_json_dump.call_args[0][0]

        assert set(stats.keys()) == {"Office", "Hotel"}

        office_stats = stats["Office"]

        # All rank columns should be present
        for col in building_cols_to_rank:
            assert col in office_stats

        # Each column should have the standard stat keys
        expected_keys = {
            "count",
            "mean",
            "min",
            "max",
            "twentyFifthPercentile",
            "median",
            "seventyFifthPercentile",
        }
        for col in building_cols_to_rank:
            assert expected_keys.issubset(set(office_stats[col].keys()))


def test_calculate_building_stats_aggregate_fields(
    property_types, grouped_by_prop_type, sample_building_data
):
    """Test that total and mean aggregate fields are correct"""
    with (
        patch(
            "src.data.scripts.generate_property_type_stats.property_stats_file_path",
            "/mock/stats/path",
        ),
        patch("builtins.open", mock_open()),
        patch("json.dump") as mock_json_dump,
    ):
        calculate_building_stats(property_types, grouped_by_prop_type)

        stats = mock_json_dump.call_args[0][0]
        office_stats = stats["Office"]

        # total for TotalGHGEmissions should be the sum of all Office buildings
        expected_total_ghg = round(
            float(
                sample_building_data[
                    sample_building_data["PrimaryPropertyType"] == "Office"
                ]["TotalGHGEmissions"].sum()
            ),
            1,
        )
        assert office_stats["TotalGHGEmissions"]["total"] == expected_total_ghg

        # total for GrossFloorArea should be the sum of all Office buildings
        expected_total_sqft = round(
            float(
                sample_building_data[
                    sample_building_data["PrimaryPropertyType"] == "Office"
                ]["GrossFloorArea"].sum()
            ),
            1,
        )
        assert office_stats["GrossFloorArea"]["total"] == expected_total_sqft

        # mean for GHGIntensity should match the average
        expected_mean_ghg = round(
            float(
                sample_building_data[
                    sample_building_data["PrimaryPropertyType"] == "Office"
                ]["GHGIntensity"].mean()
            ),
            1,
        )
        assert office_stats["GHGIntensity"]["mean"] == expected_mean_ghg


def test_calculate_building_stats_grade_distribution(
    property_types, grouped_by_prop_type
):
    """Test that grade distribution is calculated correctly"""
    with (
        patch(
            "src.data.scripts.generate_property_type_stats.property_stats_file_path",
            "/mock/stats/path",
        ),
        patch("builtins.open", mock_open()),
        patch("json.dump") as mock_json_dump,
    ):
        calculate_building_stats(property_types, grouped_by_prop_type)

        stats = mock_json_dump.call_args[0][0]

        # Office has grades A, B, C (one each)
        assert stats["Office"]["gradeDistribution"] == {"A": 1, "B": 1, "C": 1}

        # Hotel has grades B, C (one each)
        assert stats["Hotel"]["gradeDistribution"] == {"B": 1, "C": 1}


def test_calculate_building_stats_count_is_int(property_types, grouped_by_prop_type):
    """Test that count is returned as int, not float"""
    with (
        patch(
            "src.data.scripts.generate_property_type_stats.property_stats_file_path",
            "/mock/stats/path",
        ),
        patch("builtins.open", mock_open()),
        patch("json.dump") as mock_json_dump,
    ):
        calculate_building_stats(property_types, grouped_by_prop_type)

        stats = mock_json_dump.call_args[0][0]
        for prop_type in stats:
            for col in building_cols_to_rank:
                if col in stats[prop_type]:
                    assert isinstance(stats[prop_type][col]["count"], int)


@pytest.fixture
def data_center_buildings():
    """
    6 Data Center buildings mirroring the real data count: 4 reported in 2023 (latest year),
    2 reported only in 2022. Used to verify rankings are scoped to the latest year only.
    """
    return pd.DataFrame(
        {
            "PrimaryPropertyType": ["Data Center"] * 6,
            "DataYear": [2023, 2023, 2023, 2023, 2022, 2022],
            "GHGIntensity": [70.6, 135.1, 17.4, 101.7, 24.6, 50.0],
            "TotalGHGEmissions": [7338.4, 48295.3, 1620.0, 21619.7, 3131.7, 5000.0],
            "ElectricityUse": [
                52447370.0,
                361001180.0,
                11520122.0,
                154514878.7,
                20766738.4,
                30000000.0,
            ],
            "NaturalGasUse": [515230.0, 4254608.9, 0.0, 2384919.45, 333992.45, 100000.0],
            "GrossFloorArea": [160000.0, 474979.0, 65904.0, 180000.0, 104000.0, 120000.0],
            "SourceEUI": [1412.0, 2704.0, 347.9, 2129.2, 491.9, 600.0],
            "SiteEUI": [504.3, 965.7, 139.0, 761.1, 177.1, 250.0],
            "AvgPercentileLetterGrade": ["C", "F", "A", "D", "B", "C"],
            # Required by benchmarking_string_cols
            "PropertyName": ["DC1", "DC2", "DC3", "DC4", "DC5", "DC6"],
            "ChicagoEnergyRating": ["", "", "", "", "", ""],
            "ZIPCode": ["60601", "60602", "60603", "60604", "60605", "60606"],
            "Latitude": ["41.8", "41.9", "41.7", "41.85", "41.82", "41.78"],
            "Longitude": ["-87.6", "-87.7", "-87.5", "-87.65", "-87.62", "-87.58"],
            # Required by benchmarking_int_cols
            "NumberOfBuildings": [1, 1, 1, 1, 1, 1],
            "ENERGYSTARScore": [50, 30, 80, 40, 60, 55],
        }
    )


def test_rank_only_applies_to_latest_year_buildings(data_center_buildings):
    """Buildings that did not report in the latest year should receive no rank."""
    building_data = data_center_buildings.copy()
    latest_year = building_data["DataYear"].max()  # 2023
    latest_building_data = building_data[building_data["DataYear"] == latest_year]
    latest_year_grouped = latest_building_data.groupby("PrimaryPropertyType")

    with patch("src.data.scripts.generate_property_type_stats.output_to_csv"):
        rank_buildings_by_property_type(building_data, latest_year_grouped)

    latest_rows = building_data[building_data["DataYear"] == 2023]
    older_rows = building_data[building_data["DataYear"] == 2022]

    # All 4 latest-year Data Centers should have a rank
    assert latest_rows["GHGIntensityRankByPropertyType"].notna().all()
    # The 2 buildings that only reported in 2022 should have no rank
    assert older_rows["GHGIntensityRankByPropertyType"].isna().all()


def test_rank_assigns_rank_1_to_highest_emitter(data_center_buildings):
    """The building with the highest GHG intensity should receive rank 1."""
    building_data = data_center_buildings.copy()
    latest_year = building_data["DataYear"].max()
    latest_building_data = building_data[building_data["DataYear"] == latest_year]
    latest_year_grouped = latest_building_data.groupby("PrimaryPropertyType")

    with patch("src.data.scripts.generate_property_type_stats.output_to_csv"):
        rank_buildings_by_property_type(building_data, latest_year_grouped)

    latest_rows = building_data[building_data["DataYear"] == 2023]
    # GHGIntensity values for 2023: [70.6, 135.1, 17.4, 101.7] — 135.1 is highest
    highest_idx = latest_rows["GHGIntensity"].idxmax()
    assert latest_rows.loc[highest_idx, "GHGIntensityRankByPropertyType"] == 1


def test_rank_covers_all_latest_year_buildings(data_center_buildings):
    """All 4 latest-year Data Centers should receive distinct ranks 1–4."""
    building_data = data_center_buildings.copy()
    latest_year = building_data["DataYear"].max()
    latest_building_data = building_data[building_data["DataYear"] == latest_year]
    latest_year_grouped = latest_building_data.groupby("PrimaryPropertyType")

    with patch("src.data.scripts.generate_property_type_stats.output_to_csv"):
        rank_buildings_by_property_type(building_data, latest_year_grouped)

    latest_rows = building_data[building_data["DataYear"] == 2023]
    ranks = sorted(latest_rows["GHGIntensityRankByPropertyType"].tolist())
    assert ranks == [1.0, 2.0, 3.0, 4.0]


def test_calculate_building_stats_missing_property_type(grouped_by_prop_type):
    """Test that a property type not in the data is skipped"""
    with (
        patch(
            "src.data.scripts.generate_property_type_stats.property_stats_file_path",
            "/mock/stats/path",
        ),
        patch("builtins.open", mock_open()),
        patch("json.dump") as mock_json_dump,
    ):
        property_types_with_extra = ["Office", "Hotel", "NonExistentType"]
        calculate_building_stats(property_types_with_extra, grouped_by_prop_type)

        stats = mock_json_dump.call_args[0][0]
        assert "NonExistentType" not in stats
        assert "Office" in stats
        assert "Hotel" in stats
