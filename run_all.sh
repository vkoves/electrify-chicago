###
### Our Data Pipeline - This shell script contains all of the Python scripts that we use to go from
### the source Chicago Data Portal CSV export to the final CSV and JSON files we use, including
### overall rankings, rankings by property type, and separate JSON files of the city-wide and
### property type specific averages, medians, and so forth
###

# /bin/bash

python3 -m src.data.scripts.clean_and_pare_down_data_all_years

python3 -m src.data.scripts.process_data

python3 -m src.data.scripts.add_context_by_property_type

python3 -m src.data.scripts.clean_and_pare_down_data_current_year