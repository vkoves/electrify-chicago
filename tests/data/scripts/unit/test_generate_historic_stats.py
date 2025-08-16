import pytest
import pandas as pd
from pandas.testing import assert_series_equal
from unittest.mock import patch, mock_open, MagicMock
from src.data.scripts.generate_historic_stats import (
  calculateBuildingStatsByYear,
  building_cols_to_analyze
)

@pytest.fixture
def sample_building_data():
  """Create sample building data for testing"""
  data = {
    'DataYear': [2016, 2017, 2018, 2019, 2020, 2016, 2017, 2018, 2019, 2020],
    'GHGIntensity': [10.5, 12.3, 8.9, 15.2, 11.1, 20.0, 18.5, 22.1, 19.8, 16.7],
    'TotalGHGEmissions': [1000, 1200, 890, 1520, 1110, 2000, 1850, 2210, 1980, 1670],
    'ElectricityUse': [500, 600, 445, 760, 555, 1000, 925, 1105, 990, 835],
    'NaturalGasUse': [300, 360, 267, 456, 333, 600, 555, 663, 594, 501],
    'SourceEUI': [50.5, 55.2, 48.9, 62.3, 52.1, 75.0, 70.5, 78.1, 73.8, 68.7],
    'SiteEUI': [40.5, 45.2, 38.9, 52.3, 42.1, 65.0, 60.5, 68.1, 63.8, 58.7],
    'DistrictSteamUse': [0, 0, 0, 0, 0, 100, 95, 105, 98, 92],
    'DistrictChilledWaterUse': [0, 0, 0, 0, 0, 50, 48, 52, 49, 46]
  }
  return pd.DataFrame(data)

@pytest.fixture
def sample_building_data_with_pre_2016():
    """Create sample building data that includes years before 2016 (should be filtered out)"""
    data = {
        'DataYear': [2014, 2015, 2016, 2017, 2018, 2014, 2015, 2016, 2017, 2018],
        'GHGIntensity': [5.0, 6.0, 10.5, 12.3, 8.9, 8.0, 9.0, 20.0, 18.5, 22.1],
        'TotalGHGEmissions': [500, 600, 1000, 1200, 890, 800, 900, 2000, 1850, 2210],
        'ElectricityUse': [250, 300, 500, 600, 445, 400, 450, 1000, 925, 1105],
        'NaturalGasUse': [150, 180, 300, 360, 267, 240, 270, 600, 555, 663],
        'SourceEUI': [25.5, 30.2, 50.5, 55.2, 48.9, 40.0, 45.0, 75.0, 70.5, 78.1],
        'SiteEUI': [20.5, 25.2, 40.5, 45.2, 38.9, 35.0, 40.0, 65.0, 60.5, 68.1],
        'DistrictSteamUse': [0, 0, 0, 0, 0, 0, 0, 100, 95, 105],
        'DistrictChilledWaterUse': [0, 0, 0, 0, 0, 0, 0, 50, 48, 52]
    }
    return pd.DataFrame(data)


@pytest.fixture
def empty_building_data():
  """Create empty building data for edge case testing"""
  columns = [
    'DataYear', 'GHGIntensity', 'TotalGHGEmissions', 'ElectricityUse',
    'NaturalGasUse', 'SourceEUI', 'SiteEUI', 'DistrictSteamUse', 'DistrictChilledWaterUse'
  ]
  return pd.DataFrame(columns=columns)

def test_calculateBuildingStatsByYear_basic_functionality(sample_building_data):
  """Test basic functionality of calculateBuildingStatsByYear"""
  with patch('src.data.scripts.generate_historic_stats.get_data_file_path') as mock_get_path, \
       patch('builtins.open', mock_open()) as mock_file, \
       patch('json.dump') as mock_json_dump:

    # mock the file paths
    mock_get_path.side_effect = ['/mock/dist/path', '/mock/debug/path']

    # call the function
    result = calculateBuildingStatsByYear(sample_building_data)

    # verify function returns the expected paths
    assert result == ['/mock/dist/path', '/mock/debug/path']

    # verify files were opened for writing
    assert mock_file.call_count == 2

    # verify JSON was dumped twice (once minified, once with indent)
    assert mock_json_dump.call_count == 2

    # get the data that was written to JSON
    call_args = mock_json_dump.call_args_list

    # first call should be minified data (separators specified)
    minified_data = call_args[0][0][0]  # first argument of first call
    minified_separators = call_args[0][1].get('separators')
    assert minified_separators == (',', ':')

    # second call should be indented
    indented_data = call_args[1][0][0]  # first argument of second call
    indent_value = call_args[1][1].get('indent')
    assert indent_value == 4

    # both should contain the same data
    assert minified_data == indented_data

def test_calculateBuildingStatsByYear_data_structure(sample_building_data):
  """Test the structure and content of the generated statistics"""
  with patch('src.data.scripts.generate_historic_stats.get_data_file_path') as mock_get_path, \
       patch('builtins.open', mock_open()) as mock_file, \
       patch('json.dump') as mock_json_dump:
    
    mock_get_path.side_effect = ['/mock/dist/path', '/mock/debug/path']
    
    calculateBuildingStatsByYear(sample_building_data)

    # get the data structure that was written
    yearly_stats = mock_json_dump.call_args_list[0][0][0]

    # should have stats for years 2016 - 2020
    expected_years = ['2016', '2017', '2018', '2019', '2020']
    assert set(yearly_stats.keys()) == set(expected_years)

    # check the structure of one year's data
    year_2016_stats = yearly_stats['2016']

    # should have all columns we analyze
    assert set(year_2016_stats.keys()) == set(building_cols_to_analyze)

    # check that each column has the expected statistical measures
    expected_stats = ['count', 'mean', 'std', 'min', 'max', 'twentyFifthPercentile', 'median', 'seventyFifthPercentile']

    for col in building_cols_to_analyze:
      assert set(year_2016_stats[col].keys()) == set(expected_stats)

      # verify count is correct (2 buildings in sample data)
      assert year_2016_stats[col]['count'] == 2

      # verify all values are rounded to 1 decimal by checking they're not more precise
      for stat_name, stat_value in year_2016_stats[col].items():
        if stat_name != 'count': # count should be an integer
          # convert to string and check decimal places
          str_val = str(stat_value)
          if '.' in str_val:
              decimal_places = len(str_val.split('.')[1])
              assert decimal_places <= 1, f"Value {stat_value} has more than 1 decimal place"

def test_calculateBuildingStatsByYear_filters_pre_2016(sample_building_data_with_pre_2016):
  """Test that years before 2016 are filtered out"""
  with patch('src.data.scripts.generate_historic_stats.get_data_file_path') as mock_get_path, \
       patch('builtins.open', mock_open()) as mock_file, \
       patch('json.dump') as mock_json_dump:

    mock_get_path.side_effect = ['/mock/dist/path', '/mock/debug/path']

    calculateBuildingStatsByYear(sample_building_data_with_pre_2016)

    yearly_stats = mock_json_dump.call_args_list[0][0][0]

    # we should only have years 2016 and later, not 2014 and 2015
    expected_years = ['2016', '2017', '2018']
    assert set(yearly_stats.keys()) == set(expected_years)

    # should not contain 2014 or 2015
    assert '2014' not in yearly_stats
    assert '2015' not in yearly_stats


def test_calculateBuildingStatsByYear_empty_data(empty_building_data):
  """Test behavior with empty data"""
  with patch('src.data.scripts.generate_historic_stats.get_data_file_path') as mock_get_path, \
       patch('builtins.open', mock_open()) as mock_file, \
       patch('json.dump') as mock_json_dump:

    mock_get_path.side_effect = ['/mock/dist/path', '/mock/debug/path']

    result = calculateBuildingStatsByYear(empty_building_data)

    assert result == ['/mock/dist/path', '/mock/debug/path']

    # should write empty stats
    yearly_stats = mock_json_dump.call_args_list[0][0][0]
    assert yearly_stats == {}

def test_calculateBuildingStatsByYear_single_year_single_building():
  """Test with just one year and one building"""
  single_data = pd.DataFrame({
    'DataYear': [2020],
    'GHGIntensity': [15.5],
    'TotalGHGEmissions': [1550],
    'ElectricityUse': [775],
    'NaturalGasUse': [465],
    'SourceEUI': [62.5],
    'SiteEUI': [52.5],
    'DistrictSteamUse': [0],
    'DistrictChilledWaterUse': [0]
  })

  with patch('src.data.scripts.generate_historic_stats.get_data_file_path') as mock_get_path, \
       patch('builtins.open', mock_open()) as mock_file, \
       patch('json.dump') as mock_json_dump:
    
    mock_get_path.side_effect = ['/mock/dist/path', '/mock/debug/path']

    calculateBuildingStatsByYear(single_data)

    yearly_stats = mock_json_dump.call_args_list[0][0][0]

    # should have only 2020
    assert list(yearly_stats.keys()) == ['2020']

    # for a single building, mean should equal min, max, and median
    year_stats = yearly_stats['2020']
    for col in building_cols_to_analyze:
      stats = year_stats[col]
      assert stats['count'] == 1
      assert stats['mean'] == stats['min'] == stats['max'] == stats['median']

      # standard deviation should be 0 for single value (pandas returns NaN for single value std)
      # We need to handle NaN case since pandas returns NaN for std of single value
      assert stats['std'] == 0.0 or pd.isna(stats['std'])


def test_calculateBuildingStatsByYear_data_input_not_mutated(sample_building_data): 
  """Test that the input DataFrame is not modified"""
  original_data = sample_building_data.copy()

  with patch('src.data.scripts.generate_historic_stats.get_data_file_path') as mock_get_path, \
       patch('builtins.open', mock_open()) as mock_file, \
       patch('json.dump') as mock_json_dump:
      
    mock_get_path.side_effect = ['/mock/dist/path', '/mock/debug/path']
      
    calculateBuildingStatsByYear(sample_building_data)

    # original data should be unchanged
    pd.testing.assert_frame_equal(sample_building_data, original_data)

@patch('src.data.scripts.generate_historic_stats.get_and_clean_csv')
@patch('src.data.scripts.generate_historic_stats.get_data_file_path')
@patch('src.data.scripts.generate_historic_stats.log_step_completion')
def test_main_function_integration(mock_log_step, mock_get_path, mock_get_csv, sample_building_data):
    """Test the main function integration"""
    from src.data.scripts.generate_historic_stats import main

    # mock the csv loading
    mock_get_csv.return_value = sample_building_data
    mock_get_path.return_value = '/mock/path/building-data.csv'

    with patch('src.data.scripts.generate_historic_stats.calculateBuildingStatsByYear') as mock_calc_stats, \
         patch('builtins.open', mock_open()) as mock_file, \
         patch('json.dump') as mock_json_dump:
      
      mock_calc_stats.return_value = ['/mock/dist/path', '/mock/debug/path']    

      main()

      # verify the csv was loaded
      mock_get_csv.assert_called_once()

      # verify calculateBuildingStatsByYear was called
      mock_calc_stats.assert_called()

      # verify log_step_completion was called
      mock_log_step.assert_called_with(5, ['/mock/dist/path', '/mock/debug/path'])

def test_building_cols_to_analyze_completeness():
  """Test that building_cols_to_analyze contains expected columns"""
  expected_columns = [
    'GHGIntensity',
    'TotalGHGEmissions', 
    'ElectricityUse',
    'NaturalGasUse',
    'SourceEUI',
    'SiteEUI',
    'DistrictSteamUse',
    'DistrictChilledWaterUse'
  ]

  assert building_cols_to_analyze == expected_columns

def test_calculateBuildingStatsByYear_with_missing_values():
  """Test behavior with missing/NaN values in the data"""
  data_with_nan = pd.DataFrame({
      'DataYear': [2020, 2020, 2020],
      'GHGIntensity': [10.0, None, 20.0],
      'TotalGHGEmissions': [1000, 1500, None],
      'ElectricityUse': [500, 750, 1000],
      'NaturalGasUse': [300, None, 600],
      'SourceEUI': [50.0, 62.5, 75.0],
      'SiteEUI': [40.0, 52.5, None],
      'DistrictSteamUse': [0, 50, 100],
      'DistrictChilledWaterUse': [None, 25, 50]
  })
  
  with patch('src.data.scripts.generate_historic_stats.get_data_file_path') as mock_get_path, \
       patch('builtins.open', mock_open()) as mock_file, \
       patch('json.dump') as mock_json_dump:
      
    mock_get_path.side_effect = ['/mock/dist/path', '/mock/debug/path']
      
    result = calculateBuildingStatsByYear(data_with_nan)

    # should still return paths
    assert result == ['/mock/dist/path', '/mock/debug/path']

    yearly_stats = mock_json_dump.call_args_list[0][0][0]

    # should handle NaN values in statistics calculation
    assert '2020' in yearly_stats

    # count should reflect non-null values
    year_stats = yearly_stats['2020']

    # GHGIntensity has 2 valid values out of 3
    assert year_stats['GHGIntensity']['count'] == 2

    # TotalGHGEmissions has 2 valid values out of 3
    assert year_stats['TotalGHGEmissions']['count'] == 2