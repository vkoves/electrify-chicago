"""
Building Utils - Common utilities for processing building data
"""

import re

# Columns in the benchmarking data that should be strings because they are immutable identifiers
# Also prevents parsing as number and getting NaN when the value is blank
benchmarking_string_cols = [
    'PropertyName',
    'ChicagoEnergyRating',
    'ZIPCode',
    'Latitude',
    'Longitude'
]

# Int columns that are numbers (and can get averaged) but should be rounded
benchmarking_int_cols = [
    'NumberOfBuildings',
    'ENERGYSTARScore',
    # TODO: Move to string after figuring out why the X.0 is showing up
    'Wards',
    'CensusTracts',
    'CommunityAreas',
    'HistoricalWards2003-2015'
]


def clean_property_name(name: str) -> str:
    '''Clean the title of a building, stripping out extra data, like
    "(IL1041) - Marina Towers" -> "Marina Towers"
    '''

    if len(name) == 0:
        return name

    # Drop '(IL###) - ' prefix
    name = re.sub(r'\(IL\d+\) - ', '', name)

    return name
