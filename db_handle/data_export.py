# -*- coding: utf-8 -*-

import sqlite3
import csv

"""
students: id, name, id_study
studies: id, name, degree, form
subjects: id, name, id_study, semester, test
"""

db_path = r'..\dataset\university.db'

csv_files = {
                'students': r'..\dataset\students_csv.csv', 
                'subjects': r'..\dataset\subjects_csv.csv',
                'studies':  r'..\dataset\studies_csv.csv'
            }

# You need to save csv file in utf-8 encoding and open in unt-8 too
def export_students(database, csv_file):
    print('exporting students')
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        with open(csv_file, encoding='utf-8') as file:
            csv_dict = csv.DictReader(file)
            for row in csv_dict:
                cursor.execute(
                                'INSERT INTO Students(name, id_study) VALUES (?, ?)', 
                                (row['name'], int(row['id_study']))
                              )
                connection.commit()

def export_studies(database, csv_file):
    print('exporting studies')
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        with open(csv_file, encoding='utf-8') as file:
            csv_dict = csv.DictReader(file)
            for row in csv_dict:
                cursor.execute(
                                'INSERT INTO Studies (name, degree, form) VALUES (?, ?, ?)', 
                                (row['name'], row['degree'], row['form']) 
                               )
                connection.commit()      

def export_subjects(database, csv_file):
    print('exporting subjects')
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        with open(csv_file, encoding='utf-8') as file:
            csv_dict = csv.DictReader(file)
            for row in csv_dict:
                cursor.execute(
                                'INSERT INTO Subjects (name, id_study, semester, test) VALUES (?, ?, ?, ?)', 
                                (row['name'], int(row['id_study']), int(row['semester']), row['test']) 
                               )
                connection.commit()