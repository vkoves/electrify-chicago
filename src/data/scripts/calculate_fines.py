import pandas as pd
import json

def calculate_fines(file_path='../dist/benchmarking-all-years.csv', output_file='../dist/fines-by-year.json'):
    FINE_AMOUNT = 9200

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

    print(json.dumps(fines_dict, indent=2))

    with open(output_file, 'w') as f:
        json.dump(fines_dict, f, indent=2)

    print(f"\nResults saved to '{output_file}'")

calculate_fines()


