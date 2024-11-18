import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.scripts.emissions_utils import (
    update_carbon_intensity,
    calculate_electricity_emissions,
    calculate_building_emissions,
    CARBON_INTENSITY_FACTORS
)
import pandas as pd

def main():
    # Update carbon intensity values for recent years
    # Using example values - these should be replaced with actual values
    update_carbon_intensity(2020, 150)  # 150 g/kWh
    update_carbon_intensity(2021, 145)  # 145 g/kWh
    update_carbon_intensity(2022, 140)  # 140 g/kWh
    update_carbon_intensity(2023, 137)  # 137 g/kWh as per PJM Illinois report
    
    print("\nCarbon Intensity Factors:")
    for year in sorted(CARBON_INTENSITY_FACTORS.keys()):
        print(f"{year}: {CARBON_INTENSITY_FACTORS[year]} g/kWh")
        
    # Test with sample building data
    data = {
        'DataYear': [2020, 2021, 2022, 2023],
        'ElectricityUse': [100000, 100000, 100000, 100000],  # Same usage (kBtu) across years
        'PropertyName': ['Test Building'] * 4
    }
    df = pd.DataFrame(data)
    
    # Calculate emissions
    result = calculate_building_emissions(df)
    
    print("\nSample Building Emissions:")
    print("Year | Electricity (kBtu) | Electricity (kWh) | Emissions (metric tons)")
    print("-" * 65)
    for _, row in result.iterrows():
        print(f"{row['DataYear']} | {row['ElectricityUse']:>15.0f} | {row['ElectricityUseKWh']:>14.0f} | {row['ElectricityEmissions']:>19.2f}")

if __name__ == "__main__":
    main()
