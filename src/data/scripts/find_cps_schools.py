import csv

cps_schools:[str, str] = {}

with open('src/data/source/ChicagoEnergyBenchmarking.csv', newline='') as csvfile:
    whole_file = csv.DictReader(csvfile)
    for row in whole_file:
        if "CPS" in row["Property Name"]:
            cps_schools[row["ID"]] = row["Property Name"]

    for id, school in cps_schools.items():
        cleaned_school_name = school.removesuffix("-CPS").strip()  
        print("// "+cleaned_school_name)
        print('"' + id + '"' + ": { owner: BuildingOwners.cps.key },")