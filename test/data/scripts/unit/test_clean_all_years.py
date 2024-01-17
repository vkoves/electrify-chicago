import pytest
import shutil, os

from src.data.scripts import clean_and_pare_down_data_all_years as clean

src_dir = "..../src/data/source"
test_src_dir = "..../test/data/source"
file_to_copy = "ChicagoEnergyBenchmarking.csv"

@pytest.fixture
def get_dest_file():
    os.path.join(test_src_dir, file_to_copy)

@pytest.fixture
def copy_file():
    src_file_path = os.path.join(src_dir, file_to_copy)
    dest_file_path = os.path.join(test_src_dir, file_to_copy)
    if not os.path.exists(src_file_path):
        shutil.copy(src_file_path, dest_file_path)
    return file_to_copy

@pytest.fixture
def building_data(copy_file):
    pass

@pytest.mark.parametrize("test_input", [
    clean.string_cols,
    clean.int_cols,
    clean.replace_headers
])
def test_is_not_empty(test_input):
    assert len(test_input) > 0

def test_main():
    pass
