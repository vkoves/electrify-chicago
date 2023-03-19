import json
import logging
import pandas

from typing import List
from utils import get_and_clean_csv, json_data_builder

# Assume run in /data
data_directory = './source/';
data_out_directory = './dist/';

# The /debug directory is to have a well formatted JSON for reading
data_debug_directory = './debug/';

# Gatsby doesn't like spaces so we use a CSV with renamed headers with no units
building_emissions_file = 'BenchmarkDataRenamed.csv';
building_emissions_file_out_name = 'building-benchmarks'

# Columns we want to run statistical analysis and ranking on - order matters here
building_cols_to_analyze =  [
    'GHGIntensity',
    'TotalGHGEmissions',
    'ElectricityUse',
    'NaturalGasUse',
    'SourceEUI',
    'SiteEUI',
    'YearBuilt',
    'GrossFloorArea'
]

# Returns the output file if succeeds
def calculateBuildingAverages(building_data: pandas.DataFrame) -> str:
    # Clone the input data to prevent manipulating it on accident
    data = building_data.copy()

    benchmark_stats_df = pandas.DataFrame()

    # Convert our columns to average to numeric data, first by stripping commas
    data[building_cols_to_analyze] = data[building_cols_to_analyze].apply(
         lambda x: pandas.to_numeric(x.astype(str).str.replace(',',''), errors='coerce'))

    # The details columns we want to keep. Note that 50% = median
    detail_cols_to_keep = [ 'mean', 'min', 'max', '25%', '50%', '75%' ]

    benchmark_stats_df = data[building_cols_to_analyze].describe().loc[detail_cols_to_keep]

    # Round all data to an int, all of the building data is pretty large values so the precision
    # isn't reasonable for statistical analysis
    benchmark_stats_df = benchmark_stats_df.round(0).astype(int)

    # Write out the data
    filename = 'building-benchmark-stats.json';

    outputted_path = data_out_directory + filename

    # Write the minified JSON to the dist directory and indented JSON to the debug directory
    benchmark_stats_df.to_json(outputted_path)
    benchmark_stats_df.to_json(data_debug_directory + filename, indent=4)

    return outputted_path


# Returns the output file path if it succeeds
def processBuildingData() -> List[str]:
    # Store files we write out to
    outputted_paths = []

    building_data = get_and_clean_csv(data_directory + building_emissions_file)

    outputted_paths.append(calculateBuildingAverages(building_data))

    ## TODO: Individual Building Stats to Calculate
    # Rank for building_cols_to_analyze including percentage
    # E.g Keating Hall is the #1 building by GHG Intensity, and lowest 25th percentile in footprint

    # df['default_rank'] = df['Number_legs'].rank()

    # Export the data
    output_path = data_out_directory + building_emissions_file_out_name + '.csv'

    building_data.to_csv(output_path, sep=',', encoding='utf-8', index=False)

    outputted_paths.append(output_path)

    debug_json_data = json_data_builder(
        building_data, 'building_benchmarks', is_array=True, array_key="building_benchmarks")

    # We write out files to a /debug directory that is .gitignored with indentation to
    # make it readable but to not have to store giant files
    with open(
        data_debug_directory + building_emissions_file_out_name + '.json', 'w', encoding='utf-8') as f:
            json.dump(debug_json_data, f, ensure_ascii=True, indent=4)

    return outputted_paths

if __name__ == '__main__':
    print("Starting data processing, this may take a few seconds...")

    outputted_paths = []

    outputted_paths = outputted_paths + processBuildingData()

    print("\nData processing done! Files exported: ")

    for path in outputted_paths:
        if path:
            print('- ' + path)

    print('\nFor more understandable data, see \'data/debug\' directory');
