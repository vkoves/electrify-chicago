import os, pathlib, sys
import pandas as pd, numpy as np
from typing import List
from src.data.scripts.utils import get_and_clean_csv

property_test_cases = ['United Center', 'Crown Hall', 'Art Institute']

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

    src_data = get_and_clean_csv(src_path)
    test_data = get_test_sample(src_data, property_test_cases)
    print('Copied source data from', src_path)
    print('Copied test data to', copy_test_data_sample(test_data, target_path))

if __name__ == "__main__":
    main()
