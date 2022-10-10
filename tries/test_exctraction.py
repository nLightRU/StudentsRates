import csv

with open('subjects_csv.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        if row['id_fields_of_study'] == '39':
            print(row['name'], row['semester'])