import tkinter as tk
from tkinter import ttk

import models

root = tk.Tk()
root.title('Students Rates')
root.geometry('800x600+150+150')

tabControl = ttk.Notebook(root)

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

studiesSearched = []
subjectObjs = []

def study_find(debug=False):
    if debug:
        print('Search btn clicked')
        
    rows = models.session.query(models.Studies).all()
    search_str = studySearch.get()

    studiesSearched.clear()
    for row in rows:
        if search_str in row.name:
            studiesSearched.append(row)

    if debug:
        for row in studiesSearched:
            print(row.name, row.form)

    studyRows = tk.Variable(value=[row.name + ' ' + row.form for row in studiesSearched])

    studyList.config(listvariable=studyRows)


def find_subjects(debug=False):
    """
        this should return list of subjects for a given study
    """
    if debug:
        print('Find Subject button clicked')
        print('study:', studyList.curselection())

    studyIndex = studyList.curselection()[0]

    studyObj = studiesSearched[studyIndex]

    if debug:
        print('Find subjects for', studyObj.name, studyObj.form, 'id:', studyObj.id)

    q = models.session.query(models.Subjects) \
                      .where(models.Subjects.id_study == studyObj.id) \
                      .order_by(models.Subjects.semester)


    subjectsObjs = q.all()

    subjNamesList = [subj.name + ' ' + str(subj.semester) for subj in subjectsObjs]

    if debug:
        for subj in subjNamesList:
            print(subj)

    subjNames = tk.Variable(value=subjNamesList)
    
    subjectsList.config(listvariable=subjNames)


def subj_stat(debug=True):
    """
        This function should make statistics of
        subject for a given study
    """
    subj_idx = subjectsList.curselection()[0]
    if debug:
        print(subj_idx)
        print(subjectObjs)
        # print(subjectObjs[subj_idx])
    # subj_obj = subjectObjs[subj_idx]
    # statList.config(text='Статистика по предмету' + subj_obj.name)


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

statList = tk.LabelFrame(statFrame, text='Статистика гуся')
statList.pack(anchor=tk.N)

# Degree statistics GUI
degreeTab = ttk.Frame(tabControl)
tabControl.add(degreeTab, text='Уровень образования')

tabControl.pack(fill='x')

root.mainloop()

