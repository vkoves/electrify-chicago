import pytest, pathlib, os
import numpy as np
from src.data.scripts.utils import get_and_clean_csv

property_test_cases = ['United Center']

def get_file_path(dir: str, f: str):
    curr_path = pathlib.Path('.')
    path = curr_path.parent.absolute() / dir / 'data' / 'source' / f
    return path

@pytest.fixture(scope='session')
def src_data():
    file_path = get_file_path('src', 'ChicagoEnergyBenchmarking.csv')
    return get_and_clean_csv(file_path)

@pytest.fixture(scope='session')
def test_data_has_relevant_sample(src_data):
    # check that all test cases exist at least once in data set
    contains_test_cases = []
    for p in property_test_cases:
        has_related_name = src_data['Property Name'].map(lambda x: True if p in str(x) else False)
        contains_test_cases.append(np.any(has_related_name))
    assert np.all(contains_test_cases)
    test_cases = src_data['Property Name'].str.contains('|'.join(property_test_cases), na=False)
    return src_data[test_cases]

@pytest.fixture(scope='session')
def save_test_src(test_data_has_relevant_sample):
    file_path = get_file_path('test', 'test_src_data.csv')
    assert len(test_data_has_relevant_sample) > 0
    if not os.path.exists(file_path):
        test_data_has_relevant_sample.to_csv(file_path)
    return file_path