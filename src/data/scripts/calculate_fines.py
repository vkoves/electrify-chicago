import pandas as pd
import json
from src.data.scripts.utils import log_step_completion

def calculate_fines(file_path='../dist/benchmarking-all-years.csv', output_file='../dist/fines-by-year.json'):
    FINE_AMOUNT = 9200
    debug = False

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: '{file_path}' not found. Please make sure the file is in the same directory.")
        return

    not_submitted = df[df['ReportingStatus'] == 'Not Submitted']

    yearly_counts = not_submitted.groupby('DataYear').size()
    yearly_fines = yearly_counts * FINE_AMOUNT

    fines_dict = yearly_fines.to_dict()
    total_fine = sum(fines_dict.values())
    fines_dict['total'] = total_fine

    if debug:
        print(json.dumps(fines_dict, indent=2))

    with open(output_file, 'w') as f:
        json.dump(fines_dict, f, indent=2)

    if debug:
        print(f"\nResults saved to '{output_file}'")

def main():
    # Calculate fines based on non-submission
    calculate_fines()

    # Log completion of this step
    log_step_completion(6, calculate_fines())

if __name__ == "__main__":
    main()


