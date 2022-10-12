######### Statistics lists #########

# count top 10 and last 10 students
#   1 Ivan Ivanov Math rate: 100
#   2 Katya Denisova Biology rate: 90

# count study rate
# count rate: study + subject (results sheet) (DONE)

# count rate by 

import sys
import db_schema as schema

####
# TO DO: database requestst for GUI
####

#### 
# Study statistics 
#   adcademic plan
#   examinations in study with semester
#   sheet results 
####

def get_academic_plan(study=1) ->list:
    q = schema.session.query(schema.SubjectsTable.name)
    rows_unordered = q.filter(schema.SubjectsTable.id_study == study)
    rows = rows_unordered.order_by(schema.SubjectsTable.semester)
    out = []
    for row in rows:
        out.append(row.name)
    return out

def get_examinations(study=1, semester=1):
    """
    Returns a list of dicts
    {id, name, test}, {id, name. test}
    """
    q = schema.session.query(schema.SubjectsTable.id, 
                             schema.SubjectsTable.name, 
                             schema.SubjectsTable.test)
    
    exams = q.filter(schema.SubjectsTable.id_study == study,
                    schema.SubjectsTable.semester == semester)
    
    examinations = []
    
    for exam in exams:
        examinations.append({'id':exam.id, 'name':exam.name, 'test':exam.test})

    return examinations

def get_sheet_header(id_subject: int) -> dict:
    rows = schema.session.query(schema.SubjectsTable)
    subject = rows.filter(schema.SubjectsTable.id == id_subject).first()

    q = schema.session.query(schema.StudiesTable)
    study = q.filter(schema.StudiesTable.id == subject.id_study).first()

    header = {'study': study.name, 
              'subject':subject.name, 
              'semester':subject.semester, 
              'test':subject.test
              }

    return header 


def get_sheet_results(id_subject: int) -> list:
    """
    Returns list of dictionaries with students
    """
    q = schema.session.query(schema.SubjectsTable)
    subject = q.filter(schema.SubjectsTable.id == id_subject).first()

    q = schema.session.query(schema.StudentsTable)
    rows = q.filter(schema.StudentsTable.id_study == subject.id_study, 
                    schema.StudentsTable.semester == subject.semester)

    students = rows.order_by(schema.StudentsTable.name).all()
    students_list = []
    for student in students:
        q = schema.session.query(schema.ResultsTable)
        test = q.filter(schema.ResultsTable.id_student == student.id).first()

        s = {'id':student.id, 'name':student.name, 'result':test.result}
        students_list.append(s)

    return students_list

#### 
# STUDENT 
#   Student's examinations sheet
#   Rate  
####

def get_student_results(id_student: int) -> dict:
    """
    Returns student's results in dict
    {'sub_1':res_1, 'sub_2':res_2} 
    subjects that student with id_student is passed
    """
    q= schema.session.query(schema.StudentsTable)
    student = q.filter(schema.StudentsTable.id == id_student).first()
    id_study = student.id_study
    semester = student.semester

    # Get subjects
    q = schema.session.query(schema.SubjectsTable)
    rows = q.filter(schema.SubjectsTable.id_study == id_study, 
                    schema.SubjectsTable.semester <= semester)
    subjects = rows.order_by(schema.SubjectsTable.semester).all()
    
    student_results = {}

    print(student.name, student.semester, 'семестр')
    # Get results
    for subject in subjects:
        q = schema.session.query(schema.ResultsTable)
        obj = q.filter(schema.ResultsTable.id_subject == subject.id).first()
        result = obj.result
        print(subject.name, subject.semester, 'семестр', '|', 'оценка', result)

    return student_results

def count_student_rate(id_student: int) -> int:
    """
    Returns student's rate in form of percent
    passed subjects / total subjects
    """
    exam_results = {'неуд': 0, 'уд': 3, 'хор':4, 'отл':5}
    test_results = {'Незачет': 0, 'Зачет': 3}

    q = schema.session.query(schema.ResultsTable)
    rows = q.filter(schema.ResultsTable.id_student == id_student).all()
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

    ### Trace
    q = schema.session.query(schema.StudentsTable)
    obj = q.filter(schema.StudentsTable.id == id_student)
    student_name = obj.first().name
    print(student_name, 'rate:', round(rate,2))

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

        print('Предмет', str('"'+header['subject']+'"'))
        print(header['semester'], 'семестр', 
              header['test'])

        print('-------------')

        students = get_sheet_results(6254)
        for student in students:
            print(str(student['name']).ljust(25), student['result'])

        get_examinations(39, 3)

    if 'test-student' in sys.argv:
        count_student_rate(1163)
        get_student_results(1163)


