"""
Generates the lightweight building search index that powers the search
autocomplete (property name / address / type lookups).

This used to be built on every `gridsome build` in gridsome.server.js, but the
underlying benchmark data changes infrequently, so it's wasteful to regenerate
~3.5k records on every build. Instead we generate it here as part of the data
pipeline and commit the result to src/data/dist, like our other dist files.

We write a CSV (not JSON) so we don't repeat the column names on every one of
the ~3.5k rows, keeping the file small and giving clean per-row git diffs. Each
row stores the building `id` rather than a full URL; the frontend builds
`/building-id/:id`, which auto-redirects to the canonical `/building/:slug`
page. Using the id means we don't have to replicate Gridsome's slugify logic in
Python - the redirect resolves the canonical URL.
"""

import pandas as pd

from typing import List

from src.data.scripts.utils import (
    get_data_file_path,
    log_step_completion,
    output_to_csv,
)

out_dir = "dist"

# Input file path - the main file with one row per building
input_benchmark_data_csv_path = get_data_file_path(out_dir, "building-benchmarks.csv")

# Output file path
search_index_file_path = get_data_file_path(out_dir, "building-search-index.csv")


def build_search_index_df(building_data: pd.DataFrame) -> pd.DataFrame:
    """
    Build the search index rows (name, address, type, id) from the benchmark
    data. Missing name/address/type values become empty strings and the id is
    kept as a plain integer so it reads as e.g. `/building-id/123`.
    """

    index_df = pd.DataFrame(
        {
            "id": building_data["ID"],
            "name": building_data["PropertyName"],
            "address": building_data["Address"],
            "type": building_data["PrimaryPropertyType"],
        }
    )

    # The frontend treats these as plain strings, so fill missing values with
    # empty strings rather than letting NaN through
    string_cols = ["name", "address", "type"]
    index_df[string_cols] = index_df[string_cols].fillna("")

    index_df["id"] = index_df["id"].astype(int)

    return index_df


def generate_search_index(building_data: pd.DataFrame) -> List[str]:
    """
    Build the search index rows and write them to CSV.

    Returns the file paths written to.
    """

    index_df = build_search_index_df(building_data)

    output_to_csv(index_df, search_index_file_path)

    return [search_index_file_path]


###
### Main
###
def main() -> None:
    building_data = pd.read_csv(input_benchmark_data_csv_path)

    outputted_paths = generate_search_index(building_data)

    log_step_completion(9, outputted_paths)


if __name__ == "__main__":
    main()
