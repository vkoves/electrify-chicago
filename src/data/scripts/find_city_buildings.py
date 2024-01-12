import csv

found = []

def find_addresses():
    with open('src/data/source/City-Owned_Land_Inventory.csv') as source_file:
        city_file = csv.DictReader(source_file)
        MAIN_FILE_ADDRESS_INDEX = 4
        MAIN_FILE_ID_INDEX = 1
        
        with open('src/data/source/ChicagoEnergyBenchmarking.csv', newline='') as all_data:
            whole_file = all_data.read().splitlines()
            for i, line in enumerate(city_file):
                if line["Address"].strip() == "" or line["Property Status"] != "Owned by City":
                    continue
                for j, whole_file_line in enumerate(whole_file):
                    print(i, j)
                    address = whole_file_line.split(",")[MAIN_FILE_ADDRESS_INDEX]
                    if line["Address"].lower().strip().replace(" ", "") == address.lower().strip().replace(" ", ""):
                        found.append(whole_file_line.split(",")[MAIN_FILE_ID_INDEX])
                        break
                
                if i%50 == 49:
                    print(found)
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
                print(line["ID"] + ": { owner: BuildingOwners.cityofchicago.key },")
                found.remove(line["ID"])

find_addresses()
print_tags()