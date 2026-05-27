import pathlib
import sys
import csv
from typing import List
from tests.data.scripts.utils import get_test_file_path, get_src_file_path

src_dir = "src"
test_dir = "tests"
src_input_file = "ChicagoEnergyBenchmarking.csv"
test_input_file = "test_src_data.csv"

property_ids_to_include = [
    "100856",  # United Center
    "256419",  # Crown Hall
    "160196",  # The Art Institute of Chicago
    "138730",  # random property
    "240068",  # random property w/ submitted data and no GHGIntensity data
    "251245",  # random property w/ 2022 GHGIntensity data
]


def write_test_sample(
    reader: csv.reader, writer: csv.writer, property_ids_to_include: List[str]
) -> csv.writer:
    header_row = next(reader)
    if len(header_row) <= 0:
        raise EOFError("ChicagoEnergyBenchmarking CSV file is empty!")
    else:
        writer.writerow(header_row)
    for row in reader:
        property_id = row[1]
        if property_id in property_ids_to_include:
            writer.writerow(row)


def main() -> None:
    # the first console argument is technically the python script so we skip that
    src_arg = sys.argv[1]
    target_arg = sys.argv[2]
    curr_path = pathlib.Path(".").parent.absolute()
    src_path = curr_path / src_arg
    target_path = curr_path / target_arg

    csvfile = open(get_src_file_path(src_path), "r")
    src_csv = csv.reader(csvfile)

    csvfile = open(get_test_file_path(target_path), "w")
    test_file = csv.writer(csvfile)
    write_test_sample(src_csv, test_file, property_ids_to_include)
    print("Copied source data from", src_path)
    print("Copied test data to", target_path)


if __name__ == "__main__":
    main()
