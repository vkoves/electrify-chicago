import pytest
import shutil, os
import pandas as pd

from src.data.scripts import clean_and_pare_down_data_all_years as clean

src_dir = "..../src/data/source"
test_src_dir = "..../test/data/source"
file_to_copy = "ChicagoEnergyBenchmarking.csv"

@pytest.fixture
def get_src_file_path():
    return os.path.join(src_dir, file_to_copy)

@pytest.fixture
def get_dest_file_path():
    return os.path.join(test_src_dir, file_to_copy)

@pytest.fixture
def copy_file(get_src_file_path, get_dest_file_path):
    if not os.path.exists(get_src_file_path):
        shutil.copy(get_src_file_path, get_dest_file_path)
    return get_dest_file_path

@pytest.fixture
def building_data(copy_file):
    return pd.read_csv(copy_file)

@pytest.mark.parametrize("test_input", [
    clean.string_cols,
    clean.int_cols,
    clean.replace_headers
])
def test_is_not_empty(test_input):
    assert len(test_input) > 0

def test_main():
    pass
