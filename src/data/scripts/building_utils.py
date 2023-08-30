###
### Building Utils - Common utilities for processing building data
###
import re
import logging

def clean_property_name(name) -> str:
    '''Clean the title of a building, stripping out extra data, like
    "(IL1041) - Marina Towers" -> "Marina Towers"
    '''

    # Drop '(IL###) - ' prefix
    name = re.sub(r'\(IL\d+\) - ', '', name)

    return name
