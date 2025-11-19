import pandas as pd
from src.data.scripts.utils import get_data_file_path

building_path = get_data_file_path("dist", "building-benchmarks.csv")
building_benchmarks = pd.read_csv(building_path)

property_ids_to_include = [
    100856,  # United Center
    256419,  # Crown Hall
    160196,  # The Art Institute of Chicago
    138730,  # random property
    251245,  # random property
    109613,  # random property
]


def test_sample_buildings_with_wards():
    # Test Ward building benchmark attribute against the City of Chicago's
    # 'Find My Ward and Alderman page':
    # https://www.chicago.gov/city/en/depts/mayor/iframe/lookup_ward_and_alderman.html
    building_benchmarks_ordered = building_benchmarks.set_index("ID")
    test_data = building_benchmarks_ordered.loc[property_ids_to_include]
    expected_wards = [27, 3, 42, 20, 46, 24]
    assert test_data["Ward"].to_list() == expected_wards
