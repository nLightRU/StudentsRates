import tkinter as tk
from tkinter import ttk

import models
import db_requests

root = tk.Tk()
root.title('University Rates')
root.geometry('640x480+150+150')

tabControl = ttk.Notebook(root)

# Studies statics GUI
studiesTab = ttk.Frame(tabControl)
tabControl.add(studiesTab, text='Специальности')

# Courses statistics GUI
coursesTab = ttk.Frame(tabControl)
tabControl.add(coursesTab, text='Курсы')

# Subjects statistics GUI

subjectsTab = ttk.Frame(tabControl)
tabControl.add(subjectsTab, text='Предметы')

subjectsSearchFrame = ttk.Frame(subjectsTab)
subjectsSearchFrame.pack(anchor=tk.W)

# Study search in Subjects tab
studySearchLabel = tk.Label(subjectsSearchFrame, text='Введите название специальности')
studySearchLabel.pack()
studySearch = tk.Entry(subjectsSearchFrame)
studySearch.pack()


# Search results
searchResultsFrame = ttk.Frame(subjectsTab)
searchResultsFrame.pack(anchor=tk.NE)

studyRows = tk.Variable(value=[1, 2, 3, 4])
studyList = tk.Listbox(subjectsSearchFrame, listvariable=studyRows)
studyList.pack()

# Filtering courses
optionsLabel = tk.Label(subjectsSearchFrame, text='Курс')
optionsLabel.pack()
filterOptions = ['Все', 1, 2, 3, 4]
filterBox = ttk.Combobox(subjectsSearchFrame, values=filterOptions)
filterBox.pack()

# Subjects List
subjectsLabel = tk.Label(subjectsSearchFrame, text='Предметы')
subjectsLabel.pack()
subjectsRows = tk.Variable(value=['a', 'b', 'c', 'd'])
subjectsList = tk.Listbox(subjectsSearchFrame, listvariable=subjectsRows)
subjectsList.pack()

# Degree statistics GUI
degreeTab = ttk.Frame(tabControl)
tabControl.add(degreeTab, text='Уровень образования')

tabControl.pack(fill='x')

root.mainloop()

