import tkinter as tk
from tkinter import ttk

import models
import db_requests

courses = ('Первый','Второй','Третий','Четвертый')

def start_search():
    print('Search', search_row.get())

def get_search_options():
    pass

def choose_option():
    option_label.config(text=option.get())

    # q = models.session.query()

    # search_list = results
    

root = tk.Tk()
root.geometry('640x480+150+105')
root.title('Proto')

# Left frame
search_frame = tk.LabelFrame(root)
search_frame.pack(side=tk.LEFT, anchor=tk.N)

options = [ 'Рейтинг специальностей', 
            'Рейтинг курсов', 
            'Предмет на специальности',
            'Предметы на степени'
        ]

# Radiobuttons for choosing stats options
option = tk.StringVar()
r_1 = tk.Radiobutton(search_frame, text=options[0], variable=option, 
                     value=options[0], command=choose_option)
r_1.pack()

r_2 = tk.Radiobutton(search_frame, text=options[1], variable=option, 
                     value=options[1], command=choose_option)
r_2.pack()

r_3 = tk.Radiobutton(search_frame, text=options[2], variable=option, 
                     value=options[2], command=choose_option)
r_3.pack()

r_4 = tk.Radiobutton(search_frame, text=options[3], variable=option, 
                     value=options[3], command=choose_option)
r_4.pack()

search_row = tk.Entry(search_frame)
search_row.pack(anchor=tk.NW, fill='x', pady=15)

search_btn = tk.Button(search_frame, text='Search', command=start_search)
search_btn.pack()

# Search results
search_options = db_requests.get_academic_plan()
search_list = tk.Variable(value=search_options)
search_res = tk.Listbox(search_frame, listvariable=search_list)
search_res.pack(anchor=tk.NW, pady=15, fill='x')

# Right frame

info_frame = tk.LabelFrame(root)
info_frame.pack(side=tk.RIGHT, anchor=tk.NW, expand=True)

option_label = tk.Label(info_frame, text='Option')
option_label.pack(anchor=tk.W)

stats = [1, 2, 3, 4, 5, 6]
data = db_requests.get_academic_plan(46)
data_list = tk.Variable(value=data)
stat_list = tk.Listbox(info_frame, listvariable=data_list, width=80)
stat_list.pack(anchor=tk.N, fill='x', expand=True)

root.mainloop()