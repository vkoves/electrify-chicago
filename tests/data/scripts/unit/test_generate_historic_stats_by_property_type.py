import pytest
import pandas as pd
from unittest.mock import patch, mock_open
from src.data.scripts.generate_historic_stats_by_property_type import (
    calculate_historic_stats_by_property_type,
)
from src.data.scripts.generate_historic_stats import building_cols_to_analyze


@pytest.fixture
def sample_building_data():
    """Multi-year data with two property types, 2 buildings each, for testing."""
    return pd.DataFrame(
        {
            "DataYear":            [2016,  2016,  2017,  2017,  2016,  2016,  2017,  2017],
            "PrimaryPropertyType": ["Office","Office","Office","Office","Hotel","Hotel","Hotel","Hotel"],
            "GHGIntensity":        [10.0,  14.0,  12.0,  16.0,  8.0,   9.0,   9.0,   11.0],
            "TotalGHGEmissions":   [1000., 1400., 1200., 1600., 800.,  900.,  900.,  1100.],
            "ElectricityUse":      [500.,  700.,  600.,  800.,  400.,  450.,  450.,  550.],
            "NaturalGasUse":       [300.,  420.,  360.,  480.,  240.,  270.,  270.,  330.],
            "SourceEUI":           [50.0,  70.0,  55.0,  75.0,  45.0,  48.0,  48.0,  58.0],
            "SiteEUI":             [40.0,  56.0,  45.0,  61.0,  35.0,  38.0,  38.0,  46.0],
            "DistrictSteamUse":    [0.0,   0.0,   0.0,   0.0,  100.,  120.,  110.,  130.],
            "DistrictChilledWaterUse": [0.0, 0.0,  0.0,   0.0,   0.0,   0.0,   0.0,   0.0],
        }
    )


def _run_and_capture(data):
    """Helper: runs calculate_historic_stats_by_property_type and returns written stats."""
    with (
        patch(
            "src.data.scripts.generate_historic_stats_by_property_type.get_data_file_path"
        ) as mock_get_path,
        patch("builtins.open", mock_open()),
        patch("json.dump") as mock_json_dump,
    ):
        mock_get_path.side_effect = ["/mock/dist/path", "/mock/debug/path"]
        result = calculate_historic_stats_by_property_type(data)
        stats = mock_json_dump.call_args_list[0][0][0]
        return result, stats


def test_output_property_types(sample_building_data):
    """Output should have one key per property type in the input data."""
    _, stats = _run_and_capture(sample_building_data)
    assert set(stats.keys()) == {"Office", "Hotel"}


def test_output_years_per_property_type(sample_building_data):
    """Each property type should have entries for all years it reported in."""
    _, stats = _run_and_capture(sample_building_data)
    assert set(stats["Office"].keys()) == {"2016", "2017"}
    assert set(stats["Hotel"].keys()) == {"2016", "2017"}


def test_pre_2016_years_excluded():
    """Years before 2016 should be filtered out."""
    data = pd.DataFrame(
        {
            "DataYear": [2015, 2016, 2017],
            "PrimaryPropertyType": ["Office", "Office", "Office"],
            "GHGIntensity": [5.0, 10.0, 12.0],
            "TotalGHGEmissions": [500.0, 1000.0, 1200.0],
            "ElectricityUse": [250.0, 500.0, 600.0],
            "NaturalGasUse": [150.0, 300.0, 360.0],
            "SourceEUI": [25.0, 50.0, 55.0],
            "SiteEUI": [20.0, 40.0, 45.0],
            "DistrictSteamUse": [0.0, 0.0, 0.0],
            "DistrictChilledWaterUse": [0.0, 0.0, 0.0],
        }
    )
    _, stats = _run_and_capture(data)
    assert "2015" not in stats["Office"]
    assert set(stats["Office"].keys()) == {"2016", "2017"}


def test_year_with_no_data_for_property_type_excluded():
    """A year where a property type has no rows should be omitted from its output."""
    data = pd.DataFrame(
        {
            "DataYear": [2016, 2017, 2016],
            "PrimaryPropertyType": ["Office", "Office", "Hotel"],
            "GHGIntensity": [10.0, 12.0, 8.0],
            "TotalGHGEmissions": [1000.0, 1200.0, 800.0],
            "ElectricityUse": [500.0, 600.0, 400.0],
            "NaturalGasUse": [300.0, 360.0, 240.0],
            "SourceEUI": [50.0, 55.0, 45.0],
            "SiteEUI": [40.0, 45.0, 35.0],
            "DistrictSteamUse": [0.0, 0.0, 0.0],
            "DistrictChilledWaterUse": [0.0, 0.0, 0.0],
        }
    )
    _, stats = _run_and_capture(data)
    # Hotel only reported in 2016
    assert set(stats["Hotel"].keys()) == {"2016"}
    assert "2017" not in stats["Hotel"]


def test_partial_nan_column_shows_only_count():
    """A column where only some buildings have data should show count=N for those N buildings.
    A column where NO buildings have data (all NaN) is omitted by pandas describe() entirely —
    either way, NaN values must never appear in the output."""
    data = pd.DataFrame(
        {
            "DataYear": [2016, 2016, 2016],
            "PrimaryPropertyType": ["Office", "Office", "Office"],
            "GHGIntensity": [10.0, 12.0, 8.0],
            "TotalGHGEmissions": [1000.0, 1200.0, 800.0],
            "ElectricityUse": [500.0, 600.0, 400.0],
            "NaturalGasUse": [300.0, 360.0, 240.0],
            "SourceEUI": [50.0, 55.0, 45.0],
            "SiteEUI": [40.0, 45.0, 35.0],
            "DistrictSteamUse": [100.0, None, None],  # only 1 of 3 has data → count=1
            "DistrictChilledWaterUse": [None, None, None],  # all NaN → omitted by describe()
        }
    )
    _, stats = _run_and_capture(data)
    year = stats["Office"]["2016"]

    # Column present in some buildings: count reflects how many had data, no NaN values
    steam = year["DistrictSteamUse"]
    assert steam["count"] == 1
    # std is NaN for single-value columns and should be dropped entirely
    assert "std" not in steam
    assert all(not (isinstance(v, float) and pd.isna(v)) for v in steam.values())

    # Column absent in all buildings: omitted entirely OR reduced to {"count": 0}
    chilled = year.get("DistrictChilledWaterUse")
    assert chilled is None or chilled == {"count": 0}


def test_nonzero_count_column_has_all_stat_keys(sample_building_data):
    """Columns with data should have the core statistical keys (std omitted if only 1 building)."""
    _, stats = _run_and_capture(sample_building_data)
    ghg = stats["Office"]["2016"]["GHGIntensity"]
    required_keys = {"count", "mean", "min", "max", "twentyFifthPercentile", "median", "seventyFifthPercentile"}
    assert required_keys.issubset(set(ghg.keys()))


def test_count_is_integer(sample_building_data):
    """count should be an int, not a float."""
    _, stats = _run_and_capture(sample_building_data)
    for prop_type in stats:
        for year in stats[prop_type]:
            for col in building_cols_to_analyze:
                count = stats[prop_type][year][col]["count"]
                assert isinstance(count, int), (
                    f"{prop_type}/{year}/{col} count is {type(count).__name__}, expected int"
                )


def test_values_rounded_to_one_decimal(sample_building_data):
    """All numeric stats (except count) should have at most 1 decimal place."""
    _, stats = _run_and_capture(sample_building_data)
    for prop_type in stats:
        for year in stats[prop_type]:
            for col, col_stats in stats[prop_type][year].items():
                for key, val in col_stats.items():
                    if key == "count":
                        continue
                    str_val = str(val)
                    if "." in str_val:
                        decimals = len(str_val.split(".")[1])
                        assert decimals <= 1, (
                            f"{prop_type}/{year}/{col}/{key} = {val} has >1 decimal place"
                        )


def test_returns_dist_and_debug_paths(sample_building_data):
    """Function should return [dist_path, debug_path]."""
    result, _ = _run_and_capture(sample_building_data)
    assert result == ["/mock/dist/path", "/mock/debug/path"]


def test_writes_same_data_to_both_files(sample_building_data):
    """Both the minified and debug JSON writes should contain identical data."""
    with (
        patch(
            "src.data.scripts.generate_historic_stats_by_property_type.get_data_file_path"
        ) as mock_get_path,
        patch("builtins.open", mock_open()),
        patch("json.dump") as mock_json_dump,
    ):
        mock_get_path.side_effect = ["/mock/dist/path", "/mock/debug/path"]
        calculate_historic_stats_by_property_type(sample_building_data)

        assert mock_json_dump.call_count == 2
        dist_data = mock_json_dump.call_args_list[0][0][0]
        debug_data = mock_json_dump.call_args_list[1][0][0]
        assert dist_data == debug_data
        assert mock_json_dump.call_args_list[1][1].get("indent") == 4
