import csv

found = set()

# Read through an export of the City of Chicago Land Inventory, filtering to only buildings with
# the status 'Owned by City' and Managing Organization = 'AIS'
#
# Source: https://data.cityofchicago.org/Community-Economic-Development/City-Owned-Land-Inventory/aksk-kvfp
#
# This script will then log the correctly formatted data, and you can copy that into
# buildings-custom-info.constant

def clean_address(address):
    return address.lower().strip().replace(" ", "").replace(".", "")

def find_addresses():
    benchmark_buildings = {}
    with open('src/data/source/City-Owned_Land_Inventory.csv') as source_file:
        city_file = csv.DictReader(source_file)
        MAIN_FILE_ADDRESS_INDEX = 4
        MAIN_FILE_ID_INDEX = 1

        for i, line in enumerate(city_file):
            if line["Property Status"] == "Owned by City" and line["Managing Organization"] == "AIS":
                benchmark_buildings[clean_address(line["Address"])] = 0 

    with open('src/data/source/ChicagoEnergyBenchmarking.csv', newline='') as all_data:
        whole_file = all_data.read().splitlines()
        for i, line in enumerate(whole_file):
            address = line.split(",")[MAIN_FILE_ADDRESS_INDEX]
            if clean_address(address) in benchmark_buildings:
                found.add(line.split(",")[MAIN_FILE_ID_INDEX])

        if i%50 == 49:
            with open("temp.txt", "w") as f:
                f.write(str(len(found)))
                f.write("/n")
                f.write(", ".join(found))

        print("found addresses: ", found.__str__(), len(found))

def print_tags():
    with open('src/data/source/ChicagoEnergyBenchmarking.csv', newline='') as all_data:
        whole_dict = csv.DictReader(all_data)

        for line in whole_dict:
            if line["ID"] in found:
                print("// "+line["Property Name"])
                print("'" + line["ID"] + "'" + ": { owner: BuildingOwners.cityofchicago.key },")
                found.remove(line["ID"])

find_addresses()
print_tags()
