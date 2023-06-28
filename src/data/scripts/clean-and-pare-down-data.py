import pandas
from utils import get_and_clean_csv

data_directory = './source/'
building_emissions_file = 'ChicagoEnergyBenchmarking.csv'

if __name__ == "__main__":
    building_data = get_and_clean_csv(data_directory + building_emissions_file)
    replace_headers = {"Data Year": "DataYear",
        "ID": "ID",
        "Property Name": "PropertyName",
        "Reporting Status": "ReportingStatus",
        "Address": "Address",
        "ZIP Code": "ZIPCode",
        "Chicago Energy Rating": "ChicagoEnergyRating",
        "Exempt From Chicago Energy Rating": "ExemptFromChicagoEnergyRating",
        "Community Area": "CommunityArea",
        "Primary Property Type": "PrimaryPropertyType",
        "Gross Floor Area - Buildings (sq ft)": "GrossFloorArea",
        "Total GHG Emissions (Metric Tons CO2e)": "TotalGHGEmissions",
        "GHG Intensity (kg CO2e/sq ft)": "GHGIntensity",
        "Year Built": "YearBuilt",
        "# of Buildings": "NumberOfBuildings",
        "Water Use (kGal)": "WaterUse",
        "ENERGY STAR Score": "ENERGYSTARScore",
        "Electricity Use (kBtu)": "ElectricityUse",
        "Natural Gas Use (kBtu)": "NaturalGasUse",
        "District Steam Use (kBtu)": "DistrictSteamUse",
        "District Chilled Water Use (kBtu)": "DistrictChilledWaterUse",
        "All Other Fuel Use (kBtu)": "AllOtherFuelUse",
        "Site EUI (kBtu/sq ft)": "SiteEUI",
        "Source EUI (kBtu/sq ft)": "SourceEUI",
        "Weather Normalized Site EUI (kBtu/sq ft)": "WeatherNormalizedSiteEUI",
        "Weather Normalized Source EUI (kBtu/sq ft)": "WeatherNormalizedSourceEUI",
        "Latitude": "Latitude",
        "Longitude": "Longitude",
        "Location": "Location",
        "Row_ID": "Row_ID",
        "Wards": "Wards",
        "Community Areas": "CommunityAreas",
        "Zip Codes": "ZipCodes",
        "Census Tracts": "CensusTracts",
        "Historical Wards 2003-2015": "HistoricalWards2003-2015" }
    building_data.rename(columns=replace_headers,inplace=True)
    latestyear = building_data["DataYear"].max()

    print(latestyear)