"""Tests for building owner mapping logic"""

import pytest
import json
from src.data.scripts.add_building_owners import parse_owner_mappings


@pytest.fixture
def sample_json_content(tmp_path):
    """Create a temporary JSON file with owner mappings"""
    content = {
        "cityofchicago": ["101920"],
        "depaul": ["251330", "119808", "101562"],
        "iit": ["256419", "256434"],
        "uchicago": ["252064", "136212"],
    }
    test_file = tmp_path / "test_owners.json"
    test_file.write_text(json.dumps(content, indent=2))
    return str(test_file)


def test_parse_simple_owner_mapping(sample_json_content):
    """Parse simple owner mappings"""
    result = parse_owner_mappings(sample_json_content)

    assert "251330" in result
    assert result["251330"] == "depaul"
    assert result["119808"] == "depaul"
    assert result["101562"] == "depaul"


def test_parse_all_owners(sample_json_content):
    """Ensure all owner mappings are parsed"""
    result = parse_owner_mappings(sample_json_content)

    assert "101920" in result
    assert result["101920"] == "cityofchicago"

    assert "252064" in result
    assert result["252064"] == "uchicago"


def test_parse_multiple_owners(sample_json_content):
    """Ensure all different owner types are present"""
    result = parse_owner_mappings(sample_json_content)

    # Check different owners are present
    assert "depaul" in result.values()
    assert "iit" in result.values()
    assert "uchicago" in result.values()
    assert "cityofchicago" in result.values()


def test_parse_returns_correct_count(sample_json_content):
    """Verify correct number of mappings parsed"""
    result = parse_owner_mappings(sample_json_content)

    # Should have 8 buildings total
    assert len(result) == 8


def test_parse_building_ids_as_strings(sample_json_content):
    """Ensure building IDs are returned as strings"""
    result = parse_owner_mappings(sample_json_content)

    for building_id in result.keys():
        assert isinstance(building_id, str)
        assert building_id.isdigit()


def test_parse_owner_keys_as_strings(sample_json_content):
    """Ensure owner keys are returned as strings"""
    result = parse_owner_mappings(sample_json_content)

    for owner_key in result.values():
        assert isinstance(owner_key, str)
        assert owner_key.isalpha()


def test_parse_empty_json(tmp_path):
    """Handle empty JSON file gracefully"""
    empty_file = tmp_path / "empty.json"
    empty_file.write_text("{}")

    result = parse_owner_mappings(str(empty_file))

    assert result == {}


def test_parse_json_with_empty_arrays(tmp_path):
    """Handle JSON with empty owner arrays"""
    content = {"depaul": [], "iit": ["256419"]}
    test_file = tmp_path / "partial.json"
    test_file.write_text(json.dumps(content))

    result = parse_owner_mappings(str(test_file))

    # Should only have the one IIT building
    assert len(result) == 1
    assert result["256419"] == "iit"
