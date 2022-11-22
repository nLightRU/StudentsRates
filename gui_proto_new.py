"""
TO DO 
    make event for studies list
    show automatically
"""

import tkinter as tk
from tkinter import ttk

import controller

root = tk.Tk()
root.title('Students Rates')
root.geometry('800x600+150+150')

tabControl = ttk.Notebook(root)
searcher = controller.SubjectsSearcher()

# Frames for every tab

# studiesTab = ttk.Frame(tabControl)
# tabControl.add(studiesTab, text='Специальности')

# coursesTab = ttk.Frame(tabControl)
# tabControl.add(coursesTab, text='Курсы')

subjectsTab = ttk.Frame(tabControl)
subjectsTab.grid()
tabControl.add(subjectsTab, text='Предметы')

# Study search in Subjects tab



def study_find(debug=False):
    if debug:
        print('Search btn clicked')
        
    searcher.find_studies(studySearchEntry.get())
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

    index = subjectsList.curselection()[0]

    sheet = searcher.get_sheet(index)

    header_str = ''
    for key in sheet:
        if type(sheet[key]) == int:
            header_str += str(sheet[key]) + ' семестр' + '\n'
        else:    
            header_str += str(sheet[key]) + '\n'
    
    out_text = header_str + '\n'.join(searcher.get_results(index))

    if 0:
        print(out_text)

    statContent.config(text=out_text)

def export_to_csv():
    file = 'out.csv'

    with open(file, 'w', encoding='utf-8') as f:
        stat_data = statContent['text'].split('\n')
        for data in stat_data[4:]:
            f.write(data + '\n')


## SEARCH SUBJECT

subjectsSearchFrame = ttk.Frame(subjectsTab, width=70)
subjectsSearchFrame.grid(row=0, column=0)

# Searching study entry field
studySearchLabel = tk.Label(subjectsSearchFrame, text='Введите название специальности')
studySearchEntry = tk.Entry(subjectsSearchFrame)
studySearchBtn = tk.Button(subjectsSearchFrame, text='Поиск', command=study_find)
studyList = tk.Listbox(subjectsSearchFrame, width=70)

studySearchLabel.grid(row=1, column=0)
studySearchEntry.grid(row=2, column=0)
studySearchBtn.grid(row=3, column=0)
studyList.grid(row=4, column=0)

# Filtering courses

subjFindBtn = tk.Button(subjectsSearchFrame, text='Предметы', command=find_subjects)
subjFindBtn.grid(row=5, column=0)

# Subjects list of study
subjectsLabel = tk.Label(subjectsSearchFrame, text='Предметы')
subjectsLabel.grid(row=6, column=0)

subjectsList = tk.Listbox(subjectsSearchFrame, width=70)
subjectsList.grid(row=7, column=0)

subjectBtn = tk.Button(subjectsSearchFrame, text='Статистика', command=subj_stat)
subjectBtn.grid(row=8, column=0)

exportBtn = tk.Button(subjectsSearchFrame, text='Экспорт в CSV', command=export_to_csv)
exportBtn.grid(row=9, column=0)
# Statistics results in subject

# statFrame = ttk.Frame(subjectsTab)
# statFrame.grid(row=0, column=1)

statContent = tk.Label(subjectsTab, text='Статистика')
statContent.grid(row=0, column=1, sticky='n')

tabControl.pack(fill='x')

root.mainloop()

