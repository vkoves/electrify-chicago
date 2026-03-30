import pytest
from pyproj import Transformer

from src.data.scripts.utils import extract_lon_lat, parse_geojson_field


# --- parse_geojson_field ---


def test_parse_geojson_field_with_dict():
    """returns the dict unchanged when passed a dict"""
    geometry = {"type": "Point", "coordinates": [-87.6, 41.8]}
    assert parse_geojson_field(geometry) == geometry


def test_parse_geojson_field_with_valid_string():
    """parses a JSON string into a dict"""
    json_str = '{"type": "Point", "coordinates": [-87.6, 41.8]}'
    result = parse_geojson_field(json_str)
    assert result == {"type": "Point", "coordinates": [-87.6, 41.8]}


def test_parse_geojson_field_with_invalid_string():
    """returns None for an unparseable string"""
    assert parse_geojson_field("not valid json") is None


def test_parse_geojson_field_with_none():
    """returns None for None input"""
    assert parse_geojson_field(None) is None


def test_parse_geojson_field_with_empty_string():
    """returns None for empty string"""
    assert parse_geojson_field("") is None


def test_parse_geojson_field_with_non_dict_json():
    """returns None when parsed JSON is not a dict (e.g. a list)"""
    assert parse_geojson_field("[1, 2, 3]") is None


# --- extract_lon_lat ---


def test_extract_lon_lat_point():
    """returns (lon, lat) directly from a Point geometry"""
    geometry = {"type": "Point", "coordinates": [-87.6298, 41.8781]}
    lon, lat = extract_lon_lat(geometry)
    assert lon == pytest.approx(-87.6298)
    assert lat == pytest.approx(41.8781)


def test_extract_lon_lat_polygon():
    """returns centroid (lon, lat) from a Polygon geometry"""
    geometry = {
        "type": "Polygon",
        "coordinates": [
            [
                [-87.63, 41.87],
                [-87.62, 41.87],
                [-87.62, 41.88],
                [-87.63, 41.88],
                [-87.63, 41.87],
            ]
        ],
    }
    lon, lat = extract_lon_lat(geometry)
    assert lon == pytest.approx(-87.625, abs=0.001)
    assert lat == pytest.approx(41.875, abs=0.001)


def test_extract_lon_lat_with_transformer():
    """converts IL State Plane (EPSG:3435) coordinates to WGS84 lon/lat"""
    transformer = Transformer.from_crs("EPSG:3435", "EPSG:4326", always_xy=True)
    # Known IL State Plane coordinates for a point near Chicago
    geometry = {"type": "Point", "coordinates": [1176000, 1901000]}
    lon, lat = extract_lon_lat(geometry, transformer)
    # Should land somewhere in the Chicago area
    assert -88.5 < lon < -87.0
    assert 41.5 < lat < 42.5


def test_extract_lon_lat_no_transformer_returns_raw():
    """without a transformer, coordinates are returned as-is"""
    geometry = {"type": "Point", "coordinates": [1176000, 1901000]}
    lon, lat = extract_lon_lat(geometry)
    assert lon == 1176000
    assert lat == 1901000
