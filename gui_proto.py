import tkinter as tk
from tkinter import ttk

import db_requests

courses = ('Первый','Второй','Третий','Четвертый')

def start_search():
    global search_row
    print('Search', search_row.get())


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

r_1 = tk.Radiobutton(search_frame, text=options[0], value=0)
r_1.pack()
r_2 = tk.Radiobutton(search_frame, text=options[1], value=0)
r_2.pack()
r_3 = tk.Radiobutton(search_frame, text=options[2], value=0)
r_3.pack()
r_4 = tk.Radiobutton(search_frame, text=options[3], value=0)
r_4.pack()

search_row = tk.Entry(search_frame)
search_row.pack(anchor=tk.NW, fill='x', pady=15)

search_btn = tk.Button(search_frame, text='Search', command=start_search)
search_btn.pack()

# Search results
results = db_requests.get_academic_plan()
list_var = tk.Variable(value=results)
search_res = tk.Listbox(search_frame, listvariable=list_var)
search_res.pack(anchor=tk.NW, pady=15, fill='x')

# Right frame

info_frame = tk.LabelFrame(root)
info_frame.pack(side=tk.RIGHT, anchor=tk.NW, expand=True)

stats = [1, 2, 3, 4, 5, 6]
data = db_requests.get_academic_plan(46)
data_list = tk.Variable(value=data)
stat_list = tk.Listbox(info_frame, listvariable=data_list, width=80)
stat_list.pack(anchor=tk.N, fill='x', expand=True)

root.mainloop()