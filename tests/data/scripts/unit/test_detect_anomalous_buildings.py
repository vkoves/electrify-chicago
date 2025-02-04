import pytest
import pandas as pd
from pandas.testing import assert_series_equal
from unittest.mock import patch
from src.data.scripts.detect_anomalous_buildings import (
    detect_anomalous_zero_gas_buildings,
    find_and_note_anomalies,
    anomaly_values,
)

def test_detect_anomalous_zero_gas_buildings():
    # Create sample historic data, with IDs 1 & 2 being anomalous, and 3 being fine
    data = {'ID': [1, 1, 1, 2, 2, 2, 3, 3, 3],
            'DataYear': [2020, 2021, 2022, 2020, 2021, 2022, 2020, 2021, 2022],
            'NaturalGasUse': [100, 110, 0, 50, 0, 55, 200, 180, 190]}
    historic_data = pd.DataFrame(data)

    anomalous_ids = detect_anomalous_zero_gas_buildings(historic_data)
    assert set(anomalous_ids) == {1, 2}  # Check that IDs 1 and 2 are flagged

    # Test with no anomalies
    data2 = {'ID': [1, 1, 1, 2, 2, 2, 3, 3, 3],
            'DataYear': [2020, 2021, 2022, 2020, 2021, 2022, 2020, 2021, 2022],
            'NaturalGasUse': [100, 110, 120, 50, 60, 55, 200, 180, 190]}
    historic_data2 = pd.DataFrame(data2)

    anomalous_ids2 = detect_anomalous_zero_gas_buildings(historic_data2)
    assert len(anomalous_ids2) == 0


# Mock detect_anomalous_zero_gas_buildings to control the returned IDs
@pytest.fixture
def mock_detect_anomalous_zero_gas_buildings(mocker):
    mock = mocker.patch("src.data.scripts.detect_anomalous_buildings.detect_anomalous_zero_gas_buildings")
    return mock

def test_find_and_note_anomalies(mock_detect_anomalous_zero_gas_buildings):
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
