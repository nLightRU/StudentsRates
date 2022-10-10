from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, Query

engine = create_engine('sqlite:///university_results.db', echo=False)
Base = declarative_base(engine)
Session = sessionmaker(bind=engine)
session = Session()

class StudiesTable(Base):
    __tablename__ = 'Studies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    degree = Column(String)
    form = Column(String)

class SubjectsTable(Base):
    __tablename__ = 'Subjects'
        
    id = Column(Integer, primary_key=True)
    name = Column(String)
    id_study = Column(Integer, ForeignKey('Studies.id'))
    semester = Column(Integer)
    test = Column(String)

class StudentsTable(Base):
    __tablename__ = 'Students'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    id_study = Column(Integer, ForeignKey('Studies.id'))
    semester = Column(Integer)

class ResultsTable(Base):
    __tablename__ = 'Results'

    id = Column(Integer, primary_key=True)
    id_student = Column(Integer, ForeignKey('Students.id'))
    id_subject = Column(Integer, ForeignKey('Subjects.id'))
    result = Column(String)
