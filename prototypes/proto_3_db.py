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
    id_students = Column(Integer, ForeignKey('Students.id'))
    id_subject = Column(Integer, ForeignKey('Subjects.id'))
    result = Column(String)


def get_students(study=1, course=6) -> list:
    # if semester == -1:
    
    q = session.query(StudentsTable)
    semesters = [course * 2 - 1, course * 2]
    rows = q.filter(StudentsTable.id_study == study, StudentsTable.semester.in_(semesters))
    out = []
    for row in rows:
        out.append(row.name)
    return out

def get_subjects(study=1) ->list:
    rows = session.query(SubjectsTable.name).filter(SubjectsTable.id_study == study).order_by(SubjectsTable.semester)
    out = []
    for row in rows:
        out.append(row.name)
    return out
    

def get_studies(number=10) -> list:
    rows = session.query(StudiesTable.name).limit(number)
    out = []
    for row in rows:
        out.append(row.name)
    return out
