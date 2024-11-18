"""
Utilities for calculating building emissions based on electricity usage and custom carbon intensity factors.
"""

from typing import Dict, Optional
import os
import yaml
import pandas as pd

def load_carbon_intensity_factors() -> Dict[int, float]:
    """
    Load carbon intensity factors from config file.
    
    Returns:
        Dictionary mapping years to carbon intensity values (g CO2/kWh)
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'emissions.yml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config['carbon_intensity_factors']

# Load carbon intensity factors from config
CARBON_INTENSITY_FACTORS = load_carbon_intensity_factors()

def update_carbon_intensity(year: int, intensity: float) -> None:
    """
    Update the carbon intensity factor for a specific year.
    
    Args:
        year: The year to update
        intensity: Carbon intensity in grams CO2 per kWh
    """
    if year not in CARBON_INTENSITY_FACTORS:
        raise ValueError(f"Invalid year: {year}. Must be between 2014 and present year")
    if intensity < 0:
        raise ValueError("Carbon intensity cannot be negative")
    
    CARBON_INTENSITY_FACTORS[year] = intensity
    
    # Update config file
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'emissions.yml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    config['carbon_intensity_factors'][year] = intensity
    
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)

def get_carbon_intensity(year: int) -> float:
    """
    Get the carbon intensity factor for a specific year.
    
    Args:
        year: The year to get the factor for
        
    Returns:
        The carbon intensity in grams CO2 per kWh
    """
    if year not in CARBON_INTENSITY_FACTORS:
        raise ValueError(f"Invalid year: {year}. Must be between 2014 and present year")
    
    return CARBON_INTENSITY_FACTORS[year]

def calculate_electricity_emissions(electricity_use: float, year: int) -> float:
    """
    Calculate CO2 emissions from electricity usage for a specific year.
    
    Args:
        electricity_use: Electricity usage in kWh
        year: The year to calculate emissions for
        
    Returns:
        CO2 emissions in metric tons
    """
    if electricity_use < 0:
        raise ValueError("Electricity usage cannot be negative")
        
    # Get carbon intensity for the year (g CO2/kWh)
    intensity = get_carbon_intensity(year)
    
    # Calculate emissions in grams CO2
    emissions_g = electricity_use * intensity
    
    # Convert to metric tons (1 metric ton = 1,000,000 grams)
    emissions_tons = emissions_g / 1_000_000
    
    return round(emissions_tons, 2)

def calculate_building_emissions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate electricity emissions for all buildings in the dataframe.
    Adds new columns for electricity emissions based on the updated carbon intensity factors.
    
    Args:
        df: Pandas DataFrame containing building data with 'ElectricityUse' and 'DataYear' columns
        
    Returns:
        DataFrame with new 'ElectricityEmissions' column added
    """
    # Create copy to avoid modifying original
    result = df.copy()
    
    # Convert kBtu to kWh (1 kBtu = 0.293071 kWh)
    result['ElectricityUseKWh'] = result['ElectricityUse'] * 0.293071
    
    # Calculate emissions for each building based on its year
    result['ElectricityEmissions'] = result.apply(
        lambda row: calculate_electricity_emissions(
            row['ElectricityUseKWh'], 
            row['DataYear']
        ),
        axis=1
    )
    
    return result
