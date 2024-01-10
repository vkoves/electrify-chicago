# /bin/bash

python3 scripts/clean_and_pare_down_data_all_years.py

python3 scripts/process_data.py

python3 scripts/add_context_by_property_type.py

python3 scripts/clean_and_pare_down_data_current_year.py