import pytest
import pandas as pd
from unittest.mock import patch
from src.data.scripts.generate_ward_stats import (
    get_latest_year,
    calculate_compliant_buildings,
    calculate_avg_building_age,
    compile_ward_stats,
)


@pytest.fixture
def sample_building_data():
    """
    Three wards of buildings across two reporting years.
    Ward 1: 2 buildings reported in 2023 (compliant), 1 reported only in 2022.
    Ward 2: 2 buildings reported in 2023; one has no YearBuilt.
    Ward 3: 1 building that last reported in 2022 (not compliant in 2023).
    """
    return pd.DataFrame(
        {
            "Ward": [1, 1, 1, 2, 2, 3],
            "DataYear": [2023, 2023, 2022, 2023, 2023, 2022],
            "TotalGHGEmissions": [1000.0, 800.0, 900.0, 2000.0, 1500.0, 500.0],
            "GHGIntensity": [5.0, 4.0, 4.5, 8.0, 6.0, 3.0],
            "GrossFloorArea": [100000.0, 80000.0, 90000.0, 200000.0, 150000.0, 50000.0],
            "YearBuilt": [1980.0, 1970.0, 1960.0, 1990.0, None, 2000.0],
        }
    )


@pytest.fixture
def empty_building_data():
    return pd.DataFrame(
        columns=[
            "Ward",
            "DataYear",
            "TotalGHGEmissions",
            "GHGIntensity",
            "GrossFloorArea",
            "YearBuilt",
        ]
    )


# --- get_latest_year ---


def test_get_latest_year_returns_max_year(sample_building_data):
    assert get_latest_year(sample_building_data) == 2023


def test_get_latest_year_returns_int(sample_building_data):
    result = get_latest_year(sample_building_data)
    assert isinstance(result, int)


def test_get_latest_year_ignores_nan():
    data = pd.DataFrame({"DataYear": [2021.0, 2022.0, None, 2023.0]})
    assert get_latest_year(data) == 2023


def test_get_latest_year_all_nan_raises():
    data = pd.DataFrame({"DataYear": [None, None, None]})
    with pytest.raises(ValueError, match="No valid DataYear values"):
        get_latest_year(data)


def test_get_latest_year_empty_dataframe_raises(empty_building_data):
    with pytest.raises(ValueError, match="No valid DataYear values"):
        get_latest_year(empty_building_data)


def test_get_latest_year_single_valid_row():
    data = pd.DataFrame({"DataYear": [2019.0]})
    assert get_latest_year(data) == 2019


# --- calculate_compliant_buildings ---


def test_compliant_buildings_counts_latest_year_only(sample_building_data):
    result = calculate_compliant_buildings(sample_building_data, 2023)
    assert result[1] == 2  # ward 1: 2 buildings reported in 2023
    assert result[2] == 2  # ward 2: 2 buildings reported in 2023


def test_compliant_buildings_excludes_older_reporters(sample_building_data):
    result = calculate_compliant_buildings(sample_building_data, 2023)
    # ward 3 only reported in 2022, so it should not appear in the series
    assert 3 not in result.index


def test_compliant_buildings_series_name(sample_building_data):
    result = calculate_compliant_buildings(sample_building_data, 2023)
    assert result.name == "Compliant Buildings"


def test_compliant_buildings_returns_series(sample_building_data):
    result = calculate_compliant_buildings(sample_building_data, 2023)
    assert isinstance(result, pd.Series)


# --- calculate_avg_building_age ---


def test_avg_building_age_basic(sample_building_data):
    result = calculate_avg_building_age(sample_building_data, 2023)
    # Ward 1: ages 43, 53, 63 → mean 53.0
    assert result[1] == pytest.approx(53.0)


def test_avg_building_age_excludes_null_yearbuilt(sample_building_data):
    result = calculate_avg_building_age(sample_building_data, 2023)
    # Ward 2: only 1 valid YearBuilt (1990), the NaN row is excluded → age = 33
    assert result[2] == pytest.approx(33.0)


def test_avg_building_age_series_name(sample_building_data):
    result = calculate_avg_building_age(sample_building_data, 2023)
    assert result.name == "Avg Building Age (years)"


def test_avg_building_age_returns_series(sample_building_data):
    result = calculate_avg_building_age(sample_building_data, 2023)
    assert isinstance(result, pd.Series)


def test_avg_building_age_all_null_yearbuilt():
    data = pd.DataFrame(
        {
            "Ward": [1, 1],
            "DataYear": [2023, 2023],
            "YearBuilt": [None, None],
        }
    )
    result = calculate_avg_building_age(data, 2023)
    # No valid YearBuilt values — ward 1 should not appear in result
    assert 1 not in result.index


# --- compile_ward_stats ---


def test_compile_ward_stats_returns_dataframe(sample_building_data):
    compliant = calculate_compliant_buildings(sample_building_data, 2023)
    avg_age = calculate_avg_building_age(sample_building_data, 2023)
    result = compile_ward_stats(sample_building_data, compliant, avg_age)
    assert isinstance(result, pd.DataFrame)


def test_compile_ward_stats_all_50_wards_present(sample_building_data):
    compliant = calculate_compliant_buildings(sample_building_data, 2023)
    avg_age = calculate_avg_building_age(sample_building_data, 2023)
    result = compile_ward_stats(sample_building_data, compliant, avg_age)
    assert len(result) == 50
    assert set(result["Ward"]) == set(range(1, 51))


def test_compile_ward_stats_column_order(sample_building_data):
    compliant = calculate_compliant_buildings(sample_building_data, 2023)
    avg_age = calculate_avg_building_age(sample_building_data, 2023)
    result = compile_ward_stats(sample_building_data, compliant, avg_age)
    expected_cols = [
        "Ward",
        "Compliant Buildings",
        "Total Buildings",
        "Total GHG Emissions (tons CO2 eq.)",
        "Avg GHG Intensity (kg CO2 eq./sqft)",
        "Total Square Footage",
        "Avg Building Age (years)",
    ]
    assert list(result.columns) == expected_cols


def test_compile_ward_stats_zero_compliant_for_non_latest_year_ward(
    sample_building_data,
):
    compliant = calculate_compliant_buildings(sample_building_data, 2023)
    avg_age = calculate_avg_building_age(sample_building_data, 2023)
    result = compile_ward_stats(sample_building_data, compliant, avg_age)
    ward3 = result[result["Ward"] == 3].iloc[0]
    assert ward3["Compliant Buildings"] == 0


def test_compile_ward_stats_compliant_buildings_is_int(sample_building_data):
    compliant = calculate_compliant_buildings(sample_building_data, 2023)
    avg_age = calculate_avg_building_age(sample_building_data, 2023)
    result = compile_ward_stats(sample_building_data, compliant, avg_age)
    assert result["Compliant Buildings"].dtype == int


def test_compile_ward_stats_total_buildings_aggregation(sample_building_data):
    compliant = calculate_compliant_buildings(sample_building_data, 2023)
    avg_age = calculate_avg_building_age(sample_building_data, 2023)
    result = compile_ward_stats(sample_building_data, compliant, avg_age)
    ward1 = result[result["Ward"] == 1].iloc[0]
    assert ward1["Total Buildings"] == 3  # all 3 rows, not just latest year


def test_compile_ward_stats_ghg_totals(sample_building_data):
    compliant = calculate_compliant_buildings(sample_building_data, 2023)
    avg_age = calculate_avg_building_age(sample_building_data, 2023)
    result = compile_ward_stats(sample_building_data, compliant, avg_age)
    ward1 = result[result["Ward"] == 1].iloc[0]
    assert ward1["Total GHG Emissions (tons CO2 eq.)"] == pytest.approx(2700.0)


def test_compile_ward_stats_avg_ghg_intensity(sample_building_data):
    compliant = calculate_compliant_buildings(sample_building_data, 2023)
    avg_age = calculate_avg_building_age(sample_building_data, 2023)
    result = compile_ward_stats(sample_building_data, compliant, avg_age)
    ward1 = result[result["Ward"] == 1].iloc[0]
    assert ward1["Avg GHG Intensity (kg CO2 eq./sqft)"] == pytest.approx(
        (5.0 + 4.0 + 4.5) / 3
    )


def test_compile_ward_stats_wards_with_no_buildings_are_nan(sample_building_data):
    compliant = calculate_compliant_buildings(sample_building_data, 2023)
    avg_age = calculate_avg_building_age(sample_building_data, 2023)
    result = compile_ward_stats(sample_building_data, compliant, avg_age)
    # Ward 4 has no buildings in sample data — its numeric columns should be NaN
    ward4 = result[result["Ward"] == 4].iloc[0]
    assert pd.isna(ward4["Total GHG Emissions (tons CO2 eq.)"])


# --- main ---


def test_main_calls_output_and_log(sample_building_data):
    from src.data.scripts.generate_ward_stats import main

    with (
        patch(
            "src.data.scripts.generate_ward_stats.pd.read_csv",
            return_value=sample_building_data,
        ),
        patch("src.data.scripts.generate_ward_stats.output_to_csv") as mock_output,
        patch("src.data.scripts.generate_ward_stats.log_step_completion") as mock_log,
    ):
        main()

        mock_output.assert_called_once()
        mock_log.assert_called_once()
        # log receives a list containing the output path
        log_args = mock_log.call_args[0]
        assert isinstance(log_args[1], list)
        assert len(log_args[1]) == 1


def test_main_raises_when_no_valid_year(empty_building_data):
    from src.data.scripts.generate_ward_stats import main

    with (
        patch(
            "src.data.scripts.generate_ward_stats.pd.read_csv",
            return_value=empty_building_data,
        ),
        pytest.raises(ValueError, match="No valid DataYear values"),
    ):
        main()
