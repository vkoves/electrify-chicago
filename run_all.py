import subprocess
import time


# Color codes for output
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
LIGHT_BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

def print_step_header(step_number, description):
    print(f"{LIGHT_BLUE}\nRunning Step {step_number} / 3 - {description}{NC}")
    print(f"{LIGHT_BLUE}=================================================={NC}")

def handle_error(message):
    print(f"{RED}\nError: {message}{NC}")
    exit(1)

def run_python_script(module):
    try:
        subprocess.run(["python3", "-m", module], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error running {module}: {e}{NC}")
        return False
    except FileNotFoundError:
        print(f"{RED}Error: python3 not found. Is Python 3 installed?{NC}")
        return False



def main():
    start_time = time.time_ns()

    print(f"{GREEN}Initializing data pipeline!{NC}")
    print(f"Will be running from raw file at 'source/data/ChicagoEnergyBenchmarking.csv'.")

    # Each step of our data pipeline, in order
    pipeline_steps = [
        {
            "module": "src.data.scripts.clean_and_split_data",
            "description": "clean_and_split_data"
        },
        {
            "module": "src.data.scripts.process_data",
            "description": "process_data"
        },
        {
            "module": "src.data.scripts.add_context_by_property_type",
            "description": "add_context_by_property_type"
        },
    ]

    for index, step in enumerate(pipeline_steps):
        step_num = index + 1
        print_step_header(step_num, step["description"])

        if not run_python_script(step["module"]):
            handle_error(f"Step {step_num} / {len(pipeline_steps)} failed! See logs above for info.")


    end_time = time.time_ns()
    elapsed_nanoseconds = end_time - start_time
    elapsed_time = elapsed_nanoseconds / 1000000000

    print(f"\n{GREEN}========================================{NC}")
    print(f"{GREEN}All steps completed successfully in {elapsed_time:.2f} seconds!{NC}")
    print("See output files in 'src/data/dist'.")
    print("For more understandable intermediate data CSVs and JSON building stats, see 'data/debug' directory")
    print("\nNote: You must restart `gridsome develop` for data changes to take effect.")

if __name__ == '__main__':
    main()