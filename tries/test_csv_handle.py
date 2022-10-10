import csv

# with open('test_sheet.csv', newline='') as file:
#     rows = csv.reader(file, delimiter=',')
#     for row in rows:
#         print(type(row))

with open('test_sheet_dict.csv', newline='') as file:
    # fields_names = ['id', 'name', 'salary']
    reader = csv.DictReader(file)
    for row in reader:
        print(row['id'], row['name'], row['salary'])