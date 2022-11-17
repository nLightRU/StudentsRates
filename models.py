"""
TO DO:
  make arguments checking for API
  write docstrings for API functions
  make get_students_results with join
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker

import sys

engine = create_engine('sqlite:///dataset/university_results.db', echo=False)
Base = declarative_base(engine)
Session = sessionmaker(bind=engine)
session = Session()

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
    semester = Column(Integer)

class Results(Base):
    __tablename__ = 'Results'

    id = Column(Integer, primary_key=True)
    id_student = Column(Integer, ForeignKey('Students.id'))
    id_subject = Column(Integer, ForeignKey('Subjects.id'))
    result = Column(String)


# There are two entities: Study and Student
# and all statistics relies on this two entities
# the Subject table is a "glue" between studies
# and students

"""
Requests for a Study (as entity)
  - Academic plan (all subjects)
  - Examinations (exams and test in semester)
  - Subject header
  - Results for a test or an exam
"""

def get_academic_plan(study=1) -> tuple:
    """
        Gets all subjects for a given study
        ordered by semester and name.

        Returns a tuple of names.
    """
    subjects = session.query(Subjects.name) \
                      .filter(Subjects.id_study == study) \
                      .order_by(Subjects.semester).order_by(Subjects.name)

    out = [subject.name for subject in subjects]

    return tuple(out)

def get_examinations(study: int = 1, semester: int = 1) -> tuple:
    """
        Gets all exams and tests in semester of the given study.
        Arguments:
            study - id of study
            semester - id of semester

        Returns a tuple of dicts {id, name, test}.
    """

    q = session.query(Subjects.id, Subjects.name, Subjects.test)

    exams = q.filter(Subjects.id_study == study, Subjects.semester == semester)

    examinations = []

    for exam in exams:
        examinations.append({'id': exam.id, 'name': exam.name, 'test': exam.test})

    return tuple(examinations)

# Exams and tests results

def get_subject_header(id_subject: int) -> dict:
    """
        Gets a header for any subject

    """
    rows = session.query(Subjects)
    subject = rows.filter(Subjects.id == id_subject).first()

    q = session.query(Studies)
    study = q.filter(Studies.id == subject.id_study).first()

    study_header = {
        'study': study.name,
        'subject': subject.name,
        'semester': subject.semester,
        'test': subject.test
    }

    return study_header

def get_sheet_results(id_subject: int) -> tuple:
    """
    Returns a tuple of dictionaries with students
        {id, name, result}
        {id, name, result}
    """
    q = session.query(Subjects)
    subject = q.filter(Subjects.id == id_subject).first()

    q = session.query(Students)
    rows = q.filter(Students.id_study == subject.id_study,
                    Students.semester == subject.semester)

    students = rows.order_by(Students.name).all()
    students_list = []
    for student in students:
        q = session.query(Results)
        test = q.filter(Results.id_student == student.id).first()

        s = {'id': student.id, 'name': student.name, 'result': test.result}
        students_list.append(s)

    return tuple(students_list)

def get_student_results(id_student: int) -> tuple:
    """
    Returns student's results in dict
        {'name':subj, 'sem': semester_num, 'result': result string} 
    
    Arguments:
        id_student 
    subjects that student with id_student is passed
    """
    
    # Get student 
    student = session.query(Students) \
                     .filter(Students.id == id_student) \
                     .first()

    id_study = student.id_study
    semester = student.semester

    # Get subjects
    q = session.query(Subjects)
    subjects = session.query(Subjects) \
                      .filter(Subjects.id_study == id_study, \
                              Subjects.semester <= semester) \
                      .order_by(Subjects.semester) \
                      .all()

    

    # Get results
    results = []
    for subject in subjects:
        q = session.query(Results)
        obj = q.filter(Results.id_subject == subject.id).first()
        result = { 
                    'name' : subject.name,
                    'sem' : subject.semester,
                    'result': obj.result
        }
        results.append(result)
        
    return tuple(results)


def count_student_rate(id_student: int) -> float:
    """
    Returns student's rate in form of percent
    passed subjects / total subjects
    """
    exam_results = {'неуд': 0, 'уд': 3, 'хор': 4, 'отл': 5}
    test_results = {'незачет': 0, 'зачет': 3}

    q = session.query(Results)
    rows = q.filter(Results.id_student == id_student).all()
    pts = 0
    pts_total = 0
    for row in rows:
        if row.result in exam_results:
            pts += exam_results[row.result]
            pts_total += exam_results['отл']
        elif row.result in test_results:
            pts += test_results[row.result]
            pts_total += test_results['Зачет']

    rate = (pts / pts_total) * 100

    return rate

######### TEST Study #########
# Programming with C
# id = 6254, id_study = 39, semester = 3
##############################

######### TEST Student #########
# Student 1163, id_study 39, semester 3
# Student 1164, id_study 39, semester 7
################################

if __name__ == '__main__':
    if 'test-study' in sys.argv:

        header = get_subject_header(6254)
        print(header['study'])

        print('Предмет', str('"' + header['subject'] + '"'))
        print(header['semester'], 'семестр',
              header['test'])

        print('-------------')

        students = get_sheet_results(6254)
        for student in students:
            print(str(student['name']).ljust(25), student['result'])

        get_examinations(39, 3)

    if 'test-student' in sys.argv:
        count_student_rate(1163)
        results = get_student_results(1163)

        for res in results:
            print(res['name'], res['sem'], 'семестр', 'оценка', res['result'])
