"""Tests for FirstYearReported and LastYearReported calculation logic"""

import pytest
import pandas as pd
from src.data.scripts.generate_historic_stats import calculateFirstAndLastYearReported


def test_single_year_reporting():
    """Building reported in only one year should have same first and last year"""
    df = pd.DataFrame(
        {
            "ID": ["12345"],
            "DataYear": [2023],
            "GHGIntensity": [10.5],
        }
    )

    result = calculateFirstAndLastYearReported(df)

    assert result["12345"]["FirstYearReported"] == 2023
    assert result["12345"]["LastYearReported"] == 2023


def test_multiple_years_continuous():
    """Building reported continuously across multiple years"""
    df = pd.DataFrame(
        {
            "ID": ["12345", "12345", "12345", "12345"],
            "DataYear": [2020, 2021, 2022, 2023],
            "GHGIntensity": [10.5, 11.2, 10.8, 11.5],
        }
    )

    result = calculateFirstAndLastYearReported(df)

    assert result["12345"]["FirstYearReported"] == 2020
    assert result["12345"]["LastYearReported"] == 2023


def test_multiple_years_with_gaps():
    """Building reported in non-consecutive years"""
    df = pd.DataFrame(
        {
            "ID": ["12345", "12345", "12345"],
            "DataYear": [2018, 2020, 2023],
            "GHGIntensity": [10.5, 11.2, 11.5],
        }
    )

    result = calculateFirstAndLastYearReported(df)

    assert result["12345"]["FirstYearReported"] == 2018
    assert result["12345"]["LastYearReported"] == 2023


def test_building_with_zero_ghg():
    """Building with zero GHG intensity should not be counted"""
    df = pd.DataFrame(
        {
            "ID": ["12345", "12345", "12345"],
            "DataYear": [2020, 2021, 2022],
            "GHGIntensity": [0, 10.5, 11.2],
        }
    )

    result = calculateFirstAndLastYearReported(df)

    # Should start from 2021, not 2020 (since 2020 had zero GHG)
    assert result["12345"]["FirstYearReported"] == 2021
    assert result["12345"]["LastYearReported"] == 2022


def test_building_with_null_ghg():
    """Building with null GHG intensity should not be counted"""
    df = pd.DataFrame(
        {
            "ID": ["12345", "12345", "12345"],
            "DataYear": [2020, 2021, 2022],
            "GHGIntensity": [None, 10.5, 11.2],
        }
    )

    result = calculateFirstAndLastYearReported(df)

    # Should start from 2021, not 2020 (since 2020 had null GHG)
    assert result["12345"]["FirstYearReported"] == 2021
    assert result["12345"]["LastYearReported"] == 2022


def test_building_with_all_invalid_data():
    """Building with no valid reporting data should not be included"""
    df = pd.DataFrame(
        {
            "ID": ["12345", "12345"],
            "DataYear": [2020, 2021],
            "GHGIntensity": [0, None],
        }
    )

    result = calculateFirstAndLastYearReported(df)

    # Building should not be in results at all
    assert "12345" not in result


def test_multiple_buildings():
    """Multiple buildings with different reporting patterns"""
    df = pd.DataFrame(
        {
            "ID": ["111", "111", "222", "222", "222", "333"],
            "DataYear": [2020, 2023, 2019, 2020, 2021, 2023],
            "GHGIntensity": [10.5, 11.2, 8.5, 9.0, 9.5, 15.0],
        }
    )

    result = calculateFirstAndLastYearReported(df)

    # Building 111: reported 2020 and 2023
    assert result["111"]["FirstYearReported"] == 2020
    assert result["111"]["LastYearReported"] == 2023

    # Building 222: reported 2019-2021 continuously
    assert result["222"]["FirstYearReported"] == 2019
    assert result["222"]["LastYearReported"] == 2021

    # Building 333: only reported in 2023
    assert result["333"]["FirstYearReported"] == 2023
    assert result["333"]["LastYearReported"] == 2023


def test_new_building_in_latest_year():
    """Building that first reported in 2023 (new to LatestUpdates page)"""
    df = pd.DataFrame(
        {
            "ID": ["99999"],
            "DataYear": [2023],
            "GHGIntensity": [12.5],
        }
    )

    result = calculateFirstAndLastYearReported(df)

    assert result["99999"]["FirstYearReported"] == 2023
    assert result["99999"]["LastYearReported"] == 2023


def test_stopped_reporting_building():
    """Building that stopped reporting (last reported in 2022, not 2023)"""
    df = pd.DataFrame(
        {
            "ID": ["88888", "88888", "88888"],
            "DataYear": [2020, 2021, 2022],
            "GHGIntensity": [10.0, 10.5, 11.0],
        }
    )

    result = calculateFirstAndLastYearReported(df)

    assert result["88888"]["FirstYearReported"] == 2020
    assert result["88888"]["LastYearReported"] == 2022
