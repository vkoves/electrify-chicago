"""Tests for the building search index generation logic"""

import numpy as np
import pandas as pd
import pytest

from src.data.scripts.generate_search_index import build_search_index_df


@pytest.fixture
def sample_building_data():
    """Minimal benchmark data with the columns the search index needs"""
    return pd.DataFrame(
        {
            "PropertyName": ["Willis Tower", "", np.nan],
            "Address": ["233 S Wacker Dr", "300 N LaSalle", np.nan],
            "PrimaryPropertyType": ["Office", "Office", np.nan],
            "ID": [100, 200, 300],
            # An extra column that should be dropped from the index
            "GHGIntensity": [1.0, 2.0, 3.0],
        }
    )


def test_keeps_only_index_columns(sample_building_data):
    """Only name, address, type, and id are included"""
    result = build_search_index_df(sample_building_data)

    assert list(result.columns) == ["id", "name", "address", "type"]


def test_maps_source_columns(sample_building_data):
    """Source columns are renamed to the frontend field names"""
    result = build_search_index_df(sample_building_data)

    first = result.iloc[0]
    assert first["name"] == "Willis Tower"
    assert first["address"] == "233 S Wacker Dr"
    assert first["type"] == "Office"
    assert first["id"] == 100


def test_missing_values_become_empty_strings(sample_building_data):
    """NaN name/address/type become empty strings, not null/NaN"""
    result = build_search_index_df(sample_building_data)

    last = result.iloc[2]
    assert last["name"] == ""
    assert last["address"] == ""
    assert last["type"] == ""


def test_id_is_integer(sample_building_data):
    """IDs stay integers so paths read as /building-id/100, not /100.0"""
    result = build_search_index_df(sample_building_data)

    assert result["id"].dtype == "int64"
    assert [str(building_id) for building_id in result["id"]] == ["100", "200", "300"]


def test_preserves_row_count_and_order(sample_building_data):
    """Every building is included, in the original order"""
    result = build_search_index_df(sample_building_data)

    assert len(result) == 3
    assert list(result["id"]) == [100, 200, 300]
