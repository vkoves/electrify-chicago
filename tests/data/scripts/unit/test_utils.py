import json
import pandas as pd
import pytest
from pyproj import Transformer

from src.data.scripts.utils import (
    apply_verified_coordinates,
    extract_lon_lat,
    fetch_geojson_coordinates,
    parse_geojson_field,
)


# --- fetch_geojson_coordinates ---


def test_fetch_geojson_coordinates_valid_file(tmp_path):
    """returns parsed geojson dict from a valid file"""
    data = {"type": "FeatureCollection", "features": []}
    geojson_file = tmp_path / "test.geojson"
    geojson_file.write_text(json.dumps(data))

    result = fetch_geojson_coordinates(str(geojson_file))
    assert result == data


def test_fetch_geojson_coordinates_missing_file():
    """returns None when the file does not exist"""
    result = fetch_geojson_coordinates("/nonexistent/path/file.geojson")
    assert result is None


def test_fetch_geojson_coordinates_preserves_features(tmp_path):
    """returns features intact from the geojson file"""
    data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"building_id": 1},
                "geometry": {"type": "Point", "coordinates": [-87.63, 41.88]},
            }
        ],
    }
    geojson_file = tmp_path / "test.geojson"
    geojson_file.write_text(json.dumps(data))

    result = fetch_geojson_coordinates(str(geojson_file))
    assert result is not None
    assert len(result["features"]) == 1
    assert result["features"][0]["properties"]["building_id"] == 1


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


# --- apply_verified_coordinates ---


def make_building_df(rows: list[dict]) -> pd.DataFrame:
    """Helper to build a minimal building DataFrame for testing"""
    return pd.DataFrame(rows)


def make_geojson(features: list[dict]) -> dict:
    return {"type": "FeatureCollection", "features": features}


def test_apply_verified_coordinates_no_geojson():
    """tests that original data is returned when geojson is absent"""
    df = make_building_df(
        [
            {
                "ID": 1,
                "Latitude": 41.88,
                "Longitude": -87.63,
                "Location": "(41.88, -87.63)",
            }
        ]
    )

    result = apply_verified_coordinates(df, None)
    assert result.loc[0, "Longitude"] == pytest.approx(-87.63)
    assert result.loc[0, "Latitude"] == pytest.approx(41.88)
    assert result.loc[0, "Location"] == "(41.88, -87.63)"


def test_apply_verified_coordinates_wgs84_point():
    """overrides lat/lon/location from a WGS84 Point in properties.geojson"""
    df = make_building_df(
        [{"ID": 1, "Latitude": 0.0, "Longitude": 0.0, "Location": "(0.0, 0.0)"}]
    )
    geojson = make_geojson(
        [
            {
                "type": "Feature",
                "properties": {
                    "building_id": 1,
                    "geojson": '{"type": "Point", "coordinates": [-87.63, 41.88]}',
                },
                "geometry": None,
            }
        ]
    )
    result = apply_verified_coordinates(df, geojson)
    assert result.loc[0, "Longitude"] == pytest.approx(-87.63)
    assert result.loc[0, "Latitude"] == pytest.approx(41.88)
    assert result.loc[0, "Location"] == "(41.88, -87.63)"


def test_apply_verified_coordinates_state_plane_fallback():
    """falls back to IL State Plane geometry when properties.geojson is absent"""
    df = make_building_df(
        [{"ID": 1, "Latitude": 0.0, "Longitude": 0.0, "Location": "(0.0, 0.0)"}]
    )
    geojson = make_geojson(
        [
            {
                "type": "Feature",
                "properties": {"building_id": 1, "geojson": None},
                "geometry": {"type": "Point", "coordinates": [1176000, 1901000]},
            }
        ]
    )
    result = apply_verified_coordinates(df, geojson)
    # Should be somewhere in Chicago after transform
    assert -88.5 < result.loc[0, "Longitude"] < -87.0
    assert 41.5 < result.loc[0, "Latitude"] < 42.5


def test_apply_verified_coordinates_no_geometry_leaves_row_unchanged():
    """rows with no matching geojson geometry are left unchanged"""
    df = make_building_df(
        [
            {
                "ID": 1,
                "Latitude": 41.88,
                "Longitude": -87.63,
                "Location": "(41.88, -87.63)",
            }
        ]
    )
    geojson = make_geojson(
        [
            {
                "type": "Feature",
                "properties": {"building_id": 1, "geojson": None},
                "geometry": None,
            }
        ]
    )
    result = apply_verified_coordinates(df, geojson)
    assert result.loc[0, "Latitude"] == pytest.approx(41.88)
    assert result.loc[0, "Longitude"] == pytest.approx(-87.63)
    assert result.loc[0, "Location"] == "(41.88, -87.63)"


def test_apply_verified_coordinates_unmatched_building_unchanged():
    """buildings not present in the geojson are left unchanged"""
    df = make_building_df(
        [
            {
                "ID": 99,
                "Latitude": 41.88,
                "Longitude": -87.63,
                "Location": "(41.88, -87.63)",
            }
        ]
    )
    geojson = make_geojson(
        [
            {
                "type": "Feature",
                "properties": {
                    "building_id": 1,
                    "geojson": '{"type": "Point", "coordinates": [-87.0, 42.0]}',
                },
                "geometry": None,
            }
        ]
    )
    result = apply_verified_coordinates(df, geojson)
    assert result.loc[0, "Latitude"] == pytest.approx(41.88)
    assert result.loc[0, "Longitude"] == pytest.approx(-87.63)


def test_apply_verified_coordinates_multiple_buildings():
    """only the matched building is updated when multiple buildings are present"""
    df = make_building_df(
        [
            {"ID": 1, "Latitude": 0.0, "Longitude": 0.0, "Location": "(0.0, 0.0)"},
            {
                "ID": 2,
                "Latitude": 41.88,
                "Longitude": -87.63,
                "Location": "(41.88, -87.63)",
            },
        ]
    )
    geojson = make_geojson(
        [
            {
                "type": "Feature",
                "properties": {
                    "building_id": 1,
                    "geojson": '{"type": "Point", "coordinates": [-87.70, 41.95]}',
                },
                "geometry": None,
            }
        ]
    )
    result = apply_verified_coordinates(df, geojson)
    assert result.loc[0, "Longitude"] == pytest.approx(-87.70)
    assert result.loc[0, "Latitude"] == pytest.approx(41.95)
    assert result.loc[1, "Longitude"] == pytest.approx(-87.63)
    assert result.loc[1, "Latitude"] == pytest.approx(41.88)
