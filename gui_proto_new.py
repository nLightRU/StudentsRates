import tkinter as tk
from tkinter import ttk

import controller
import models

root = tk.Tk()
root.title('Students Rates')
root.geometry('800x600+150+150')

tabControl = ttk.Notebook(root)
searcher = controller.SubjectsSearcher()

# Frames for every tab

studiesTab = ttk.Frame(tabControl)
tabControl.add(studiesTab, text='Специальности')

coursesTab = ttk.Frame(tabControl)
tabControl.add(coursesTab, text='Курсы')

subjectsTab = ttk.Frame(tabControl)
tabControl.add(subjectsTab, text='Предметы')

# Study search in Subjects tab

subjectsSearchFrame = ttk.Frame(subjectsTab)
subjectsSearchFrame.pack(anchor=tk.W)

def study_find(debug=False):
    if debug:
        print('Search btn clicked')
        
    searcher.find_studies(studySearch.get())
    studies_names = searcher.studies_rows()

    studyRows = tk.Variable(value=studies_names)

    studyList.config(listvariable=studyRows)


def find_subjects(debug=False):
    """
        this should return list of subjects for a given study
    """
    if debug:
        print('Find Subject button clicked')
        print('study:', studyList.curselection())

    studyIndex = studyList.curselection()[0]

    if debug:
        print(searcher.study(studyIndex))

    searcher.find_subjects(searcher.study(studyIndex)['id'])
    subjects = searcher.subjects_rows()

    subjNames = tk.Variable(value=subjects)
    
    subjectsList.config(listvariable=subjNames)


def subj_stat(debug=True):
    """
        This function should make statistics of
        subject for a given study
    """

    subjIndex = 0

    pass


# Searching study entry field

studySearchLabel = tk.Label(subjectsSearchFrame, text='Введите название специальности')
studySearchLabel.pack()
studySearch = tk.Entry(subjectsSearchFrame)
studySearch.pack()
studySearchBtn = tk.Button(subjectsSearchFrame, text='Поиск', command=study_find)
studySearchBtn.pack()

# Search results
studyList = tk.Listbox(subjectsSearchFrame, width=70)
studyList.pack()

# Filtering courses
optionsLabel = tk.Label(subjectsSearchFrame, text='Курс')
optionsLabel.pack()
filterOptions = ['Все', 1, 2, 3, 4]
filterBox = ttk.Combobox(subjectsSearchFrame, values=filterOptions)
filterBox.pack()
filterBtn = tk.Button(subjectsSearchFrame, text='Предметы', command=find_subjects)
filterBtn.pack()

# Subjects list of study
subjectsLabel = tk.Label(subjectsSearchFrame, text='Предметы')
subjectsLabel.pack()

subjectsList = tk.Listbox(subjectsSearchFrame, width=70)
subjectsList.pack()

subjectBtn = tk.Button(subjectsSearchFrame, text='Статистика', command=subj_stat)
subjectBtn.pack()

# Statistics results in subject

statFrame = tk.Frame(subjectsTab)
statFrame.pack(anchor=tk.E)

statList = tk.Label(statFrame, text='Статистика гуся')
statList.pack(anchor=tk.S)

# Degree statistics GUI
degreeTab = ttk.Frame(tabControl)
tabControl.add(degreeTab, text='Уровень образования')

tabControl.pack(fill='x')

root.mainloop()

