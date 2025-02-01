###
### Utils - Basic utilities for file processing that are agnostic to the specific
### data being processed
###
import pandas
import logging
import pathlib, os
from pathlib import Path

from typing import List

def get_data_file_path(dir: str, f: str) -> str:
    # get path for source data file to process
    curr_path = pathlib.Path(".")
    path = curr_path.parent.absolute() / "src" / "data" / dir / f
    return path

# Fetch a CSV and clean it up, keeping the cols_to_keep and converting the
# number_cols to numbers
def get_and_clean_csv(path_to_csv, cols_to_keep=None) -> pandas.DataFrame:
    df = pandas.read_csv(path_to_csv)

    # logging.warning(df);

    # TODO: Take in raw city CSV and rename columns per a mapping

    if cols_to_keep is None:
        return df
    else:
        return df[cols_to_keep]


# this function takes in a dataframe object, and reformats it to match our needs as a json object
def json_data_builder(
    dataframe, outer_tag="default", is_array=True, array_key="emissionsByYear"
) -> List[str]:
    '''
    Process the a CSV dataframe into a JSON object
    '''

    uniqueColKey = 'ID'

    dataframe=dataframe.applymap(lambda x: "" if pandas.isnull(x) else x)
    # initiate empty json object to iterate with
    json_object = []

    # grab list of unique states for for_loop
    unique_buildings = list(set(dataframe[uniqueColKey]))

    for building in unique_buildings:
        building_df = dataframe.loc[dataframe[uniqueColKey] == building]
        # # need to set building as the index here, so it's not duplicated in our final json
        # if is_array:
        #     building_df.set_index(uniqueColKey, inplace=True)
        #     building_json = building_df.to_dict('records')
        #     json_object.append({"building": building, array_key: building_json})
        # else:
        building_json = building_df.to_dict('records')[0]
        json_object.append(building_json)

    # Return outer tag output object
    return json_object
