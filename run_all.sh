###
### Our Data Pipeline - This shell script contains all of the Python scripts that we use to go from
### the source Chicago Data Portal CSV export to the final CSV and JSON files we use, including
### overall rankings, rankings by property type, and separate JSON files of the city-wide and
### property type specific averages, medians, and so forth
###

# /bin/bash

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
LIGHT_BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print a step header with color
print_step_header() {
  echo -e "\n${LIGHT_BLUE}========================================${NC}"
  echo -e "${LIGHT_BLUE}Running Step $1 / 3 - $2${NC}"
  echo -e "${LIGHT_BLUE}========================================${NC}"
}

# Function to handle errors
handle_error() {
  echo -e "${RED}\nError: $1${NC}"
  exit 1
}

# Step 1: clean_and_pare_down_data_all_years
print_step_header 1 "clean_and_pare_down_data_all_years"
if ! python3 -m src.data.scripts.clean_and_pare_down_data_all_years; then
  handle_error "Step 1 / 3 failed! See logs above for info."
fi

# Step 2: process_data
print_step_header 2 "process_data"
if ! python3 -m src.data.scripts.process_data; then
  handle_error "Step 2 / 3 failed! See logs above for info."
fi

# Step 3: add_context_by_property_type
print_step_header 3 "add_context_by_property_type"
if ! python3 -m src.data.scripts.add_context_by_property_type; then
  handle_error "Step 3 / 3 failed! See logs above for info."
fi

echo -e "\n${GREEN}---------------------------------${NC}"
echo -e "${GREEN}All steps completed successfully!${NC} See output files in 'src/data/dist'."
echo -e "For more understandable intermediate data CSVs and JSON building stats, see 'data/debug' directory"
echo -e "\nNote: You must restart \`gridsome develop\` for data changes to take effect."

exit 0
