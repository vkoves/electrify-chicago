import pytest
import pandas as pd
from src.data.scripts.emissions_utils import (
    update_carbon_intensity,
    get_carbon_intensity,
    calculate_electricity_emissions,
    calculate_building_emissions,
    CARBON_INTENSITY_FACTORS
)

def test_update_carbon_intensity():
    # Test valid update
    update_carbon_intensity(2014, 150)
    assert CARBON_INTENSITY_FACTORS[2014] == 150
    
    # Test invalid year
    with pytest.raises(ValueError):
        update_carbon_intensity(2013, 100)
    
    # Test negative intensity
    with pytest.raises(ValueError):
        update_carbon_intensity(2014, -10)

def test_get_carbon_intensity():
    # Set known value
    CARBON_INTENSITY_FACTORS[2014] = 140
    
    # Test valid retrieval
    assert get_carbon_intensity(2014) == 140
    
    # Test invalid year
    with pytest.raises(ValueError):
        get_carbon_intensity(2013)

def test_calculate_electricity_emissions():
    # Set known intensity
    CARBON_INTENSITY_FACTORS[2014] = 100  # 100g CO2/kWh
    
    # Test calculation (1000 kWh * 100 g/kWh = 100,000g = 0.1 metric tons)
    assert calculate_electricity_emissions(1000, 2014) == 0.1
    
    # Test negative electricity use
    with pytest.raises(ValueError):
        calculate_electricity_emissions(-100, 2014)
    
    # Test invalid year
    with pytest.raises(ValueError):
        calculate_electricity_emissions(1000, 2013)

def test_calculate_building_emissions():
    # Create test DataFrame
    data = {
        'DataYear': [2014, 2015, 2016],
        'ElectricityUse': [1000, 2000, 3000],  # kBtu
        'PropertyName': ['Building A', 'Building B', 'Building C']
    }
    df = pd.DataFrame(data)
    
    # Set known intensities
    CARBON_INTENSITY_FACTORS[2014] = 100
    CARBON_INTENSITY_FACTORS[2015] = 100
    CARBON_INTENSITY_FACTORS[2016] = 100
    
    # Calculate emissions
    result = calculate_building_emissions(df)
    
    # Check new columns exist
    assert 'ElectricityUseKWh' in result.columns
    assert 'ElectricityEmissions' in result.columns
    
    # Check kBtu to kWh conversion (1 kBtu = 0.293071 kWh)
    assert round(result.iloc[0]['ElectricityUseKWh'], 2) == round(1000 * 0.293071, 2)
    
    # Check emissions calculation
    # First building: 1000 kBtu = 293.071 kWh
    # At 100 g/kWh = 29,307.1g = 0.03 metric tons
    assert round(result.iloc[0]['ElectricityEmissions'], 2) == 0.03
