from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, Query

engine = create_engine('sqlite:///university.db', echo=False)
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

def get_students() -> list:
    records = session.query(StudentsTable.name).all()
    out = []
    for row in records:
        out.append(row.name)
    return out

def get_subjects() ->list:
    records = session.query(SubjectsTable).all()
    out = []
    for row in records:
        out.append(row.name)
    return out

def get_studies() -> list:
    records = session.query(StudiesTable).all()
    out = []
    for row in records:
        out.append(row.name)
    return out
