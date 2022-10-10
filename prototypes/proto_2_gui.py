import tkinter as tk
from tkinter import ttk

import proto_2_db as db

# UI Initialization
root = tk.Tk()
root.title('Students Rates')
root.geometry('720x480+200+200')
root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=5)
root.columnconfigure(2, weight=5)

# self.get_btn = tk.Button( self.__root__, text='Get Studies', command=self.database.get_studies)

selected_table = tk.StringVar()
combo_box = ttk.Combobox(root, textvariable=selected_table)
combo_box['values'] = ('Students', 'Subjects', 'Studies')
combo_box['state'] = 'readonly'
combo_box.grid(row=0, column=0, sticky=tk.N)

values_list = tk.Variable()
list_box = tk.Listbox(root, listvariable=values_list)
list_box.grid(row=0, column=1, columnspan=3, sticky=tk.EW)

def select_rows(event):
    table = selected_table.get()
    if table == 'Subjects':
        list_box['listvariable'] = tk.Variable(value=db.get_subjects()[:20])
    elif table == 'Students':
        list_box['listvariable'] = tk.Variable(value=db.get_students()[:20])
    elif table == 'Studies':
        list_box['listvariable'] = tk.Variable(value=db.get_studies()[:20])
    else:
        print('select rows ERROR')

combo_box.bind('<<ComboboxSelected>>', select_rows)

if __name__ == '__main__':
    root.mainloop()