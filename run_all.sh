# /bin/bash

python3 -m src.data.scripts.clean_and_pare_down_data_all_years

python3 -m src.data.scripts.process_data

python3 -m src.data.scripts.add_context_by_property_type

python3 -m src.data.scripts.clean_and_pare_down_data_current_year

python3 -m src.data.scripts.grade_buildings