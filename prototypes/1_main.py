from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, Query

import tkinter as tk

class DatabaseMapper: 
    Engine = create_engine('sqlite:///university.db', echo=False)
    Base = declarative_base(Engine)
    Session = sessionmaker()

    class Studies(Base):
        __tablename__ = 'Studies'

        id = Column(Integer, primary_key=True)
        name = Column(String)
        degree = Column(String)
        form = Column(String)

    class Subjects(Base):
        __tablename__ = 'Subjects'
        
        id = Column(Integer, primary_key=True)
        name = Column(String)
        id_study = Column(Integer, ForeignKey('Studies.id'))
        semester = Column(Integer)
        test = Column(String)

    class Students(Base):
        __tablename__ = 'Students'

        id = Column(Integer, primary_key=True)
        name = Column(String)
        id_study = Column(Integer, ForeignKey('Studies.id'))

    def __init__(self):
        self.session = self.Session(bind=self.Engine)

    def get_studies(self) -> list:
        return self.session.query(self.Studies).all()

class App: 
    __root__ = tk.Tk()

    def __init__(self):
        self.database = DatabaseMapper()
        self.init_ui()
    
    def init_ui(self):
        self.__root__.title('Students Rates')
        self.__root__.geometry('640x480+200+200')

        # self.get_btn = tk.Button( self.__root__, text='Get Studies', 
        #                           command=self.database.get_studies)

        studies_names = []
        studies_data = self.database.get_studies()
        for study in studies_data[:20]:
            studies_names.append(
                                (study.name, study.degree)
                                )

        self.studies_var = tk.Variable(value=studies_names)

        self.list_box = tk.Listbox(self.__root__, listvariable=self.studies_var)
        self.list_box.grid(row=0, column=0, columnspan=5, sticky=tk.EW, padx=10, pady=5)

    def run(self):
        self.__root__.mainloop()

app = App()
app.run()