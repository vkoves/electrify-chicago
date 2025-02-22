import pytest
import pandas as pd
from pandas.testing import assert_series_equal
from unittest.mock import patch
from src.data.scripts.detect_anomalous_buildings import (
    detect_anomalous_zero_gas_buildings,
    detect_large_gas_swing_buildings,
    find_and_note_anomalies,
    anomaly_values,
)

def test_detect_large_gas_swing_buildings_threshold_100Prcnt():
    # Building ID 1 has a huge swing (> 100%), 2 and 3 are "normal"
    # NOTE: We may want to tweak this, as doubling is a 100% increase, but cutting in half is just
    # a 50% decrease, so a 100% threshold can never be met going down
    mock_data = pd.DataFrame({
        'ID':             [1, 1, 1,     2, 2, 2,        3, 3, 3],
        'NaturalGasUse':  [10, 12, 28,  100, 110, 105,  8, 2, 1],
        'ElectricityUse': [10, 12, 28,  100, 110, 105,  8, 2, 1]
    })

    expected_ids = [1]
    anom_ids = detect_large_gas_swing_buildings(mock_data, threshold=1)

    assert sorted(anom_ids) == sorted(expected_ids)

def test_detect_large_gas_swing_buildings_with_threshold_70Prcnt():
    # Building ID 1 & 3 have large swings (> 80%), 4 has a large swing, but it's tiny compared to
    # its electric use and shouldn't be flagged
    mock_data = pd.DataFrame({
        'ID':             [1, 1, 1,     2, 2, 2,        3, 3, 3,  4, 4, 4],
        'NaturalGasUse':  [10, 12, 28,  100, 110, 105,  8, 2, 1,  6, 2, 1],
        'ElectricityUse': [4, 3, 2,     5, 6, 90,       2, 4, 2,  100, 100, 100]
    })

    expected_ids = [1, 3]
    anom_ids = detect_large_gas_swing_buildings(mock_data, threshold=0.7)
    assert sorted(anom_ids) == sorted(expected_ids)

def test_detect_large_gas_swing_buildings_with_empty_data():
    # 0 and none are basically the same thing in our data, so make sure we don't flag that
    mock_data = pd.DataFrame({
        'ID':             [1, 1, 1,        2, 2, 2,        3, 3, 3],
        'NaturalGasUse':  [0, None, None,  0, None, 0,     30, 32, 33],
        'ElectricityUse': [0, None, None,  0, None, 0,     30, 32, 33]
    })

    expected_ids = []
    anom_ids = detect_large_gas_swing_buildings(mock_data)
    assert sorted(anom_ids) == sorted(expected_ids)


def test_detect_anomalous_zero_gas_buildings():
    # Create sample historic data, with IDs 1 & 2 being anomalous, and 3 & 4 being fine, with a COVID
    # 0 blip and very negligible gas use relative to electric respectively.
    data = {
        'ID':            [1, 1, 1,           2, 2, 2,            3, 3, 3,          4, 4, 4],
        'DataYear':      [2020, 2021, 2022,  2020,  2021, 2022,  2020, 2021, 2022, 2020, 2021, 2022],
        'NaturalGasUse': [100, 110, 0,       50, 100, 0,         200, 0, 190,      3, 4, 0],
        'ElectricityUse': [100, 110, 0,       50, 100, 0,        200, 0, 190,      150, 140, 135],
    }
    historic_data = pd.DataFrame(data)

    anomalous_ids = detect_anomalous_zero_gas_buildings(historic_data)
    assert set(anomalous_ids) == {1, 2}  # Check that IDs 1 and 2 are flagged

    # Test with no anomalies
    data2 = {
        'ID':            [1, 1, 1,           2, 2, 2,           3, 3, 3],
        'DataYear':      [2020, 2021, 2022,  2020, 2021, 2022,  2020, 2021, 2022],
        'NaturalGasUse': [100, 110, 120,     50, 60, 55,        200, 180, 190],
        'ElectricityUse': [100, 110, 120,     50, 60, 55,        200, 180, 190]
    }
    historic_data2 = pd.DataFrame(data2)

    anomalous_ids2 = detect_anomalous_zero_gas_buildings(historic_data2)
    assert len(anomalous_ids2) == 0


# Mock detect_anomalous_zero_gas_buildings and detect_large_gas_swing_buildings to control the returned IDs
@pytest.fixture
def mock_detect_anomalous_zero_gas_buildings(mocker):
    mock = mocker.patch("src.data.scripts.detect_anomalous_buildings.detect_anomalous_zero_gas_buildings")
    return mock

@pytest.fixture
def mock_detect_large_gas_swing_buildings(mocker):
    mock = mocker.patch("src.data.scripts.detect_anomalous_buildings.detect_large_gas_swing_buildings")
    return mock

def test_find_and_note_anomalies(mock_detect_anomalous_zero_gas_buildings, mock_detect_large_gas_swing_buildings):
    # Sample building and historic data
    building_data = pd.DataFrame({
        'ID': [1, 2, 3, 4],
        'OtherColumn': ['A', 'B', 'C', 'D']
    })

    # Setup historic data - this doesn't matter since we mock the detect anomalous zero gas
    # buildings function
    historic_data = pd.DataFrame({
        'ID': [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4],
        'DataYear': [2020, 2021, 2022, 2020, 2021, 2022, 2020, 2021, 2022, 2020, 2021, 2022],
        'NaturalGasUse': [100, 110, 0, 50, 0, 55, 200, 180, 190, 100, 110, 120]
    })

    # Mock that buildings 2 and 4 are anomalous
    mock_detect_anomalous_zero_gas_buildings.return_value = [2, 4]
    mock_detect_large_gas_swing_buildings.return_value = []

    # ensure we copy the input data to prevent mutation
    updated_building_data = find_and_note_anomalies(building_data.copy(), historic_data)

    # Assertions
    assert 'DataAnomalies' in updated_building_data.columns

    # Confirm our anomalous buildings 2 & 4 have zero gas anomaly value
    assert updated_building_data.loc[updated_building_data['ID'] == 2, 'DataAnomalies'].iloc[0] == anomaly_values['zero_gas_but_prev_use']
    assert updated_building_data.loc[updated_building_data['ID'] == 4, 'DataAnomalies'].iloc[0] == anomaly_values['zero_gas_but_prev_use']

    # Confirm buildings 1 & 3 have empty string values
    assert updated_building_data.loc[updated_building_data['ID'] == 1, 'DataAnomalies'].iloc[0] == ''
    assert updated_building_data.loc[updated_building_data['ID'] == 3, 'DataAnomalies'].iloc[0] == ''

    # Confirm the OtherColumn is still there, untouched
    assert_series_equal(updated_building_data['OtherColumn'], building_data['OtherColumn'], check_dtype=False)
