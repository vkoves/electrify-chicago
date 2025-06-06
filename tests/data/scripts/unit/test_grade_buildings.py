import pytest
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal, assert_series_equal
from unittest.mock import patch, MagicMock

from src.data.scripts.grade_buildings import (
    generate_percentile_grade,
    generate_energy_int_grade,
    generate_energymix_grade,
    generate_consistent_reporting_grade,
    calculate_weighted_average,
    grade_ghg_intensity_energy_mix_all_years,
    grade_buildings,
    bins,
    letter_grades,
    overall_grade_weights,
    energy_mix_grade_weights
)


# Test generate_percentile_grade function
def test_generate_percentile_grade():
    # Create a test series
    test_values = pd.Series([10, 30, 50, 70, 90])

    # Test normal case (higher values are better)
    result = generate_percentile_grade(test_values, "TestCol", reverse=False)

    # Check shape and columns
    assert result.shape == (5, 2)
    assert "TestColPercentileGrade" in result.columns
    assert "TestColLetterGrade" in result.columns

    # The actual percentile values will depend on the implementation of percentileofscore
    # We'll just check they're in ascending order and in the correct range
    percentiles = result["TestColPercentileGrade"].values
    assert all(percentiles[i] <= percentiles[i+1] for i in range(len(percentiles)-1))
    assert all(0 <= p <= 100 for p in percentiles)

    # Test reverse case (lower values are better)
    result_reverse = generate_percentile_grade(test_values, "TestCol", reverse=True)

    # The percentiles should be in descending order for reverse=True
    percentiles_rev = result_reverse["TestColPercentileGrade"].values
    assert all(percentiles_rev[i] >= percentiles_rev[i+1] for i in range(len(percentiles_rev)-1))
    assert all(0 <= p <= 100 for p in percentiles_rev)


# Test grade_ghg_intensity_energy_mix_all_years function
def test_grade_ghg_intensity_energy_mix_all_years():
    # Create test data with multiple years
    test_data = pd.DataFrame({
        "ID": [1, 2, 3, 1, 2, 3],
        "DataYear": [2021, 2021, 2021, 2022, 2022, 2022],
        "GHGIntensity": [10, 20, 30, 15, 25, 35],
        "ElectricityUse": [100, 80, 60, 90, 70, 50],
        "NaturalGasUse": [0, 20, 40, 10, 30, 50],
        "DistrictSteamUse": [0, 0, 0, 0, 0, 0],
        "DistrictChilledWaterUse": [0, 0, 0, 0, 0, 0],
        "AllOtherFuelUse": [0, 0, 0, 0, 0, 0],
        "ReportingStatus": ["Submitted", "Submitted", "Submitted",
                           "Submitted", "Submitted", "Submitted"]
    })

    # Run the function
    result = grade_ghg_intensity_energy_mix_all_years(test_data)

    # Check that the result has the expected grading columns
    assert "GHGIntensityPercentileGrade" in result.columns
    assert "GHGIntensityLetterGrade" in result.columns
    assert "EnergyMixPercentileGrade" in result.columns
    assert "EnergyMixLetterGrade" in result.columns

    # Check that all original columns are preserved
    for col in test_data.columns:
        assert col in result.columns

    # Check that the data has the same number of rows
    assert len(result) == len(test_data)


# Test generate_consistent_reporting_grade function
def test_generate_consistent_reporting_grade():
    # Create test data with varying reporting statuses
    test_data = pd.DataFrame({
        "ID": [1, 1, 1, 2, 2, 2, 3, 3, 3],
        "DataYear": [2020, 2021, 2022, 2020, 2021, 2022, 2020, 2021, 2022],
        "ReportingStatus": [
            "Submitted", "Submitted", "Submitted",  # ID 1: 100% reporting
            "Submitted", "Not Submitted", "Submitted",  # ID 2: 67% reporting
            "Not Submitted", "Not Submitted", "Submitted"  # ID 3: 33% reporting
        ]
    })

    # Run the function
    result = generate_consistent_reporting_grade(test_data)

    # Check columns
    assert "SubmittedRecordsPercentileGrade" in result.columns
    assert "SubmittedRecordsLetterGrade" in result.columns
    assert "MissingRecordsCount" in result.columns

    # Check values
    # ID 1: 100% reporting = grade A
    id1_row = result[result["ID"] == 1]
    assert id1_row["SubmittedRecordsPercentileGrade"].values[0] == 100.0
    assert id1_row["SubmittedRecordsLetterGrade"].values[0] == "A"
    assert id1_row["MissingRecordsCount"].values[0] == 0

    # ID 2: 67% reporting - check it's in the expected range
    id2_row = result[result["ID"] == 2]
    assert id2_row["SubmittedRecordsPercentileGrade"].values[0] == pytest.approx(66.67, 0.1)
    # The grade depends on bins configuration, so we'll check it's a valid grade
    assert id2_row["SubmittedRecordsLetterGrade"].values[0] in letter_grades
    assert id2_row["MissingRecordsCount"].values[0] == 1

    # ID 3: 33% reporting - should be a low grade
    id3_row = result[result["ID"] == 3]
    assert id3_row["SubmittedRecordsPercentileGrade"].values[0] == pytest.approx(33.33, 0.1)
    assert id3_row["SubmittedRecordsLetterGrade"].values[0] in letter_grades
    assert id3_row["MissingRecordsCount"].values[0] == 2


# Test calculate_weighted_average function
def test_calculate_weighted_average():
    # Create test data with different grade combinations
    test_data = pd.DataFrame({
        "GHGIntensityPercentileGrade": [90, 50, 10],  # A, C, F
        "EnergyMixPercentileGrade": [90, 50, 10],     # A, C, F
        "SubmittedRecordsPercentileGrade": [90, 50, 10]  # A, C, F
    })

    # Calculate weighted average
    result = calculate_weighted_average(test_data)

    # Check results using the defined weights
    # A-grade building: 90 * 0.5 + 90 * 0.4 + 90 * 0.1 = 45 + 36 + 9 = 90
    # C-grade building: 50 * 0.5 + 50 * 0.4 + 50 * 0.1 = 25 + 20 + 5 = 50
    # F-grade building: 10 * 0.5 + 10 * 0.4 + 10 * 0.1 = 5 + 4 + 1 = 10
    expected = pd.Series([90.0, 50.0, 10.0], index=test_data.index)
    assert_series_equal(result, expected)


# Test for energy mix grading logic
def test_energy_mix_grading():
    # This test validates the energy mix grading logic more directly

    # Create test buildings with different energy mixes
    test_data = pd.DataFrame({
        "ID": [1, 2, 3, 4],
        "DataYear": [2022, 2022, 2022, 2022],
        # Building 1: 100% electricity (best)
        # Building 2: 50% electricity, 50% gas (average)
        # Building 3: 100% gas (worst)
        # Building 4: Mix of good and bad sources
        "ElectricityUse": [1000, 500, 0, 400],
        "NaturalGasUse": [0, 500, 1000, 400],
        "DistrictSteamUse": [0, 0, 0, 100],
        "DistrictChilledWaterUse": [0, 0, 0, 100],
        "AllOtherFuelUse": [0, 0, 0, 0]
    })

    # Call the function directly
    result = generate_energymix_grade(test_data, 2022)

    # Verify the expected weighted percentages
    # Building 1: 100% electricity = 100% weight
    # Building 2: 50% electricity = 50% weight
    # Building 3: 0% electricity = 0% weight
    # Building 4: 40% electricity + 10% chilled water = 50% weight
    assert result.loc[result["ID"] == 1, "EnergyMixWeightedPctSum"].iloc[0] == 100.0
    assert result.loc[result["ID"] == 2, "EnergyMixWeightedPctSum"].iloc[0] == 50.0
    assert result.loc[result["ID"] == 3, "EnergyMixWeightedPctSum"].iloc[0] == 0.0
    assert result.loc[result["ID"] == 4, "EnergyMixWeightedPctSum"].iloc[0] == 50.0


# Integration test with simple mock data
# Test that grades are generated for historical years
def test_grades_generate_historically():
    """
    Test that grades are calculated and preserved for each historical year,
    not just the latest year.
    """
    # Create historical data with multiple years
    historical_data = pd.DataFrame({
        "ID": [1, 1, 2, 2],  # Two buildings
        "DataYear": [2021, 2022, 2021, 2022],  # Two years
        "GHGIntensity": [10, 15, 20, 25],  # Different values each year
        "ElectricityUse": [1000, 900, 500, 400],  # More electric = better
        "NaturalGasUse": [0, 100, 500, 600],  # More gas = worse
        "DistrictSteamUse": [0, 0, 0, 0],
        "DistrictChilledWaterUse": [0, 0, 0, 0],
        "AllOtherFuelUse": [0, 0, 0, 0],
        "ReportingStatus": ["Submitted", "Submitted", "Submitted", "Submitted"]
    })

    # Use a simpler mock setup for this test
    with patch("pandas.read_csv", return_value=historical_data):
        # Skip mocking the intermediate functions - let them run for real
        result = grade_buildings()

        # Check that we have grades for both years
        assert len(result["DataYear"].unique()) == 2
        assert set(result["DataYear"].unique()) == {2021, 2022}

        # Check that each building has grades for each year
        for building_id in [1, 2]:
            for year in [2021, 2022]:
                # Get data for this building and year
                building_year_data = result[(result["ID"] == building_id) &
                                           (result["DataYear"] == year)]

                # Should have one row per building per year
                assert len(building_year_data) == 1

                # Should have all grade columns
                for col in ["GHGIntensityLetterGrade", "EnergyMixLetterGrade",
                           "AvgPercentileGrade", "AvgPercentileLetterGrade"]:
                    assert col in building_year_data.columns
                    assert not pd.isna(building_year_data[col].iloc[0])


def test_building_grade_examples():
    """
    Test that buildings with specific characteristics get the expected grades
    by mocking the CSV read and running the full grading function.
    """
    # Create a mock test dataset with 3 buildings:
    # - Building 1: A-grade (low GHG, all electric, perfect reporting)
    # - Building 2: C-grade (average metrics)
    # - Building 3: F-grade (high GHG, all gas, poor reporting)
    test_data = pd.DataFrame({
        "ID": [1, 2, 3],
        "DataYear": [2022, 2022, 2022],
        "GHGIntensity": [5, 15, 30],
        "ElectricityUse": [1000, 500, 0],
        "NaturalGasUse": [0, 500, 1000],
        "DistrictSteamUse": [0, 0, 0],
        "DistrictChilledWaterUse": [0, 0, 0],
        "AllOtherFuelUse": [0, 0, 0],
        "ReportingStatus": ["Submitted", "Submitted", "Submitted"]
    })

    # Create historical data for consistent reporting calculation
    historical_data = pd.DataFrame({
        "ID": [1, 1, 1, 1, 1,
              2, 2, 2, 2, 2,
              3, 3, 3, 3, 3],
        "DataYear": [2018, 2019, 2020, 2021, 2022,
                    2018, 2019, 2020, 2021, 2022,
                    2018, 2019, 2020, 2021, 2022],
        "ReportingStatus": [
            # Building 1: Perfect reporting
            "Submitted", "Submitted", "Submitted", "Submitted", "Submitted",
            # Building 2: 3/5 reporting
            "Not Submitted", "Submitted", "Submitted", "Not Submitted", "Submitted",
            # Building 3: Only reported most recent year
            "Not Submitted", "Not Submitted", "Not Submitted", "Not Submitted", "Submitted"
        ],
        "GHGIntensity": [5, 5, 5, 5, 5,  # Building 1: Low GHG
                        15, 15, 15, 15, 15,  # Building 2: Medium GHG
                        30, 30, 30, 30, 30],  # Building 3: High GHG
        "ElectricityUse": [1000, 1000, 1000, 1000, 1000,  # Building 1: All electric
                          500, 500, 500, 500, 500,  # Building 2: 50/50 mix
                          0, 0, 0, 0, 0],  # Building 3: No electric
        "NaturalGasUse": [0, 0, 0, 0, 0,  # Building 1: No gas
                         500, 500, 500, 500, 500,  # Building 2: 50/50 mix
                         1000, 1000, 1000, 1000, 1000]  # Building 3: All gas
    })

    with patch("pandas.read_csv", return_value=historical_data):
        with patch("src.data.scripts.grade_buildings.grade_ghg_intensity_energy_mix_all_years") as mock_grade:
            # Mock to simulate that:
            # - Building 1 gets A for GHG and A for energy mix
            # - Building 2 gets C for GHG and C for energy mix
            # - Building 3 gets F for GHG and F for energy mix
            mock_grade.return_value = pd.DataFrame({
                "ID": [1, 2, 3],
                "DataYear": [2022, 2022, 2022],
                "GHGIntensity": [5, 15, 30],
                "ElectricityUse": [1000, 500, 0],
                "NaturalGasUse": [0, 500, 1000],
                "DistrictSteamUse": [0, 0, 0],
                "DistrictChilledWaterUse": [0, 0, 0],
                "AllOtherFuelUse": [0, 0, 0],
                "ReportingStatus": ["Submitted", "Submitted", "Submitted"],
                "GHGIntensityPercentileGrade": [90, 50, 10],  # A, C, F
                "GHGIntensityLetterGrade": ["A", "C", "F"],
                "EnergyMixWeightedPctSum": [100, 50, 0],
                "EnergyMixPercentileGrade": [90, 50, 10],  # A, C, F
                "EnergyMixLetterGrade": ["A", "C", "F"]
            })

            # Let generate_consistent_reporting_grade return the expected values
            with patch("src.data.scripts.grade_buildings.generate_consistent_reporting_grade") as mock_reporting:
                mock_reporting.return_value = pd.DataFrame({
                    "ID": [1, 2, 3],
                    "SubmittedRecordsPercentileGrade": [100, 60, 20],
                    "SubmittedRecordsLetterGrade": ["A", "C", "F"],
                    "MissingRecordsCount": [0, 2, 4]
                })

                # Run the grading function
                result = grade_buildings()

                # Make sure the grade columns are present
                assert "AvgPercentileGrade" in result.columns
                assert "AvgPercentileLetterGrade" in result.columns

                # Check that the specific buildings got their expected grades
                a_grade_building = result[result["ID"] == 1]
                c_grade_building = result[result["ID"] == 2]
                f_grade_building = result[result["ID"] == 3]

                # Validate that building grades match expectations
                assert a_grade_building["AvgPercentileLetterGrade"].iloc[0] == "A"
                assert c_grade_building["AvgPercentileLetterGrade"].iloc[0] == "C"
                assert f_grade_building["AvgPercentileLetterGrade"].iloc[0] == "F"