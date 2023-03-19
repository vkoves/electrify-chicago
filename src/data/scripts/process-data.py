import json
import logging

from utils import get_and_clean_csv, json_data_builder

# Assume run in /data
data_directory = './source/';
data_out_directory = './dist/';

# The /debug directory is to have a well formatted JSON for reading
data_debug_directory = './debug/';

# Gatsby doesn't like spaces so we use a CSV with renamed headers with no units
building_emissions_file = 'BenchmarkDataRenamed.csv';
building_emissions_file_out_name = 'building-benchmarks'

# Returns the output file path if it succeeds
def processBuildingData() -> str:

    building_data = get_and_clean_csv(data_directory + building_emissions_file)

    output_path = data_out_directory + building_emissions_file_out_name + '.csv'

    building_data.to_csv(output_path, sep=',', encoding='utf-8', index=False)

    debug_json_data = json_data_builder(
        building_data, 'building_benchmarks', is_array=True, array_key="building_benchmarks")

    # We write out files to a /debug directory that is .gitignored with indentation to
    # make it readable but to not have to store giant files
    with open(
        data_debug_directory + building_emissions_file_out_name + '.json', 'w', encoding='utf-8') as f:
            json.dump(debug_json_data, f, ensure_ascii=True, indent=4)

    return output_path

if __name__ == '__main__':
    print("Starting data processing, this may take a few seconds...")

    outputted_paths = []

    outputted_paths.append(processBuildingData())

    print("\nData processing done! Files exported: ")

    for path in outputted_paths:
        print('- ' + path)

    print('\nFor more understandable data, see \'data/debug\' directory');
