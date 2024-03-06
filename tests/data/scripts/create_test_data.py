import os, pathlib, sys, csv
import pandas as pd, numpy as np
from typing import List
from src.data.scripts.utils import get_and_clean_csv
from tests.data.scripts.utils import get_test_file_path, get_src_file_path

src_dir = 'src'
test_dir = 'tests'
src_input_file = 'ChicagoEnergyBenchmarking.csv'
test_input_file = 'test_src_data.csv'

property_test_cases = ['United Center', 'Crown Hall', 'Art Institute', 'Marie Curie']

def write_test_sample(reader: csv.reader, writer: csv.writer, property_test_cases: List[str]) -> csv.writer:
    header_row = next(reader)
    if len(header_row) <= 0:
        raise Exception('ChicagoEnergyBenchmarking CSV file is empty!') 
    else:
        writer.writerow(header_row)
    for row in reader:
        for item in row:
            has_prop = False
            for case in property_test_cases:
                if case in item:
                    has_prop = True
                    writer.writerow(row)
                    break
            if has_prop:
                break

def get_test_sample(src_data: pd.DataFrame, property_test_cases: List[str]) -> pd.DataFrame:
    # check that all test cases exist at least once in data set
    assert len(src_data) > 0
    contains_test_cases = []
    for p in property_test_cases:
        has_related_name = src_data['Property Name'].map(lambda x: True if p in str(x) else False)
        contains_test_cases.append(np.any(has_related_name))
    assert np.all(contains_test_cases)
    test_cases = src_data['Property Name'].str.contains('|'.join(property_test_cases), na=False)
    return src_data[test_cases]

def copy_test_data_sample(
        test_data: pd.DataFrame, 
        test_data_file_path: pathlib.Path
    ) -> pathlib.Path:
    if not os.path.exists(test_data_file_path):
        os.makedirs(os.path.dirname(test_data_file_path), exist_ok=True)
        test_data.to_csv(test_data_file_path, index=False)
    return test_data_file_path

def main():
    # the first console argument is technically the python script so we skip that
    src_arg = sys.argv[1]
    target_arg = sys.argv[2]
    curr_path = pathlib.Path(".").parent.absolute()
    src_path = curr_path / src_arg
    target_path = curr_path / target_arg

    # src_data = get_and_clean_csv(src_path)
    # test_data = get_test_sample(src_data, property_test_cases)
    csvfile = open(get_src_file_path(src_path), 'r')
    src_csv = csv.reader(csvfile) 

    csvfile = open(get_test_file_path(target_path), 'w')
    test_file = csv.writer(csvfile)
    write_test_sample(src_csv, test_file, property_test_cases)
    print('Copied source data from', src_path)
    print('Copied test data to', target_path)

if __name__ == "__main__":
    main()
