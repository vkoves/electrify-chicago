# /bin/bash

python3 scripts/clean-and-pare-down-data_all_years.py

python3 scripts/process-data.py

python3 scripts/add-context-by-property-type.py

python3 scripts/clean-and-pare-down-data_current_year.py