######### Statistics lists #########

# count top 10 and last 10 students
#   1 Ivan Ivanov Math rate: 100
#   2 Katya Denisova Biology rate: 90

# count study rate
# count rate: study + subject (results sheet) (DONE)

# count rate by 

import sys
import models


####
# TO DO: database requests for GUI
####

#### 
# Study statistics 
#   academic plan
#   examinations in study with semester
#   sheet results 
####

def get_academic_plan(study=1) -> list:
    q = models.session.query(models.Subjects.name)
    rows_unordered = q.filter(models.Subjects.id_study == study)
    rows = rows_unordered.order_by(models.Subjects.semester)
    out = []
    for row in rows:
        out.append(row.name)
    return out


def get_examinations(study: int = 1, semester: int = 1) -> list:
    """
    Returns a list of dicts
    {id, name, test}, {id, name. test}
    """
    q = models.session.query(models.Subjects.id,
                             models.Subjects.name,
                             models.Subjects.test)

    exams = q.filter(models.Subjects.id_study == study,
                     models.Subjects.semester == semester)

    examinations = []

    for exam in exams:
        examinations.append({'id': exam.id, 'name': exam.name, 'test': exam.test})

    return examinations


def get_sheet_header(id_subject: int) -> dict:
    rows = models.session.query(models.Subjects)
    subject = rows.filter(models.Subjects.id == id_subject).first()

    q = models.session.query(models.Studies)
    study = q.filter(models.Studies.id == subject.id_study).first()

    study_header = {
        'study': study.name,
        'subject': subject.name,
        'semester': subject.semester,
        'test': subject.test
    }

    return study_header


def get_sheet_results(id_subject: int, debug=False) -> list:
    """
    Returns list of dictionaries with students
        {id, name, result}
        {id, name, result}
    """
    q = models.session.query(models.Subjects)
    subject = q.filter(models.Subjects.id == id_subject).first()

    q = models.session.query(models.Students)
    rows = q.filter(models.Students.id_study == subject.id_study,
                    models.Students.semester == subject.semester)

    students = rows.order_by(models.Students.name).all()
    students_list = []
    for student in students:
        q = models.session.query(models.Results)
        test = q.filter(models.Results.id_student == student.id).first()

        s = {'id': student.id, 'name': student.name, 'result': test.result}
        students_list.append(s)

    if debug:
        for student in students_list:
            print(
                str("%25s %s" % (student['name'], student['result']))
            )

    return students_list


####
# STUDENT 
#   Student's examinations sheet
#   Rate  
####

def print_student_results(id_student: int, debug=False) -> dict:
    """
    Returns student's results in dict
    {'sub_1':res_1, 'sub_2':res_2} 
    subjects that student with id_student is passed
    """
    q = models.session.query(models.Students)
    student = q.filter(models.Students.id == id_student).first()
    id_study = student.id_study
    semester = student.semester

    # Get subjects
    q = models.session.query(models.Subjects)
    rows = q.filter(models.Subjects.id_study == id_study,
                    models.Subjects.semester <= semester)
    subjects = rows.order_by(models.Subjects.semester).all()

    student_results = {}

    if debug:
        print(student.name, student.semester, 'семестр')

    # Get results
    for subject in subjects:
        q = models.session.query(models.Results)
        obj = q.filter(models.Results.id_subject == subject.id).first()
        result = obj.result
        print(subject.name, subject.semester, 'семестр', '|', 'оценка', result)

    return student_results


def count_student_rate(id_student: int) -> float:
    """
    Returns student's rate in form of percent
    passed subjects / total subjects
    """
    exam_results = {'неуд': 0, 'уд': 3, 'хор': 4, 'отл': 5}
    test_results = {'незачет': 0, 'зачет': 3}

    q = models.session.query(models.Results)
    rows = q.filter(models.Results.id_student == id_student).all()
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

        header = get_sheet_header(6254)
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
        print_student_results(1163)
