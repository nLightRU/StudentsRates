import db_handle as db

def get_students(study=1, course=6) -> list:
    # if semester == -1:
    
    q = db.session.query(db.StudentsTable)
    semesters = [course * 2 - 1, course * 2]
    rows = q.filter(db.StudentsTable.id_study == study, db.StudentsTable.semester.in_(semesters))
    out = []
    for row in rows:
        out.append(row.name)
    return out

def get_subjects(study=1) ->list:
    rows = db.session.query(db.SubjectsTable.name).filter(db.SubjectsTable.id_study == study).order_by(SubjectsTable.semester)
    out = []
    for row in rows:
        out.append(row.name)
    return out
    

def get_studies(number=10) -> list:
    rows = db.session.query(db.StudiesTable.name).limit(number)
    out = []
    for row in rows:
        out.append(row.name)
    return out

def count_student_rate(id_student: int) -> int:
    exam_results = {'неуд': 0, 'уд': 3, 'хор':4, 'отл':5}
    test_results = {'Незачёт': 0, 'Зачёт': 3}

    req = db.session.query(db.ResultsTable).filter(db.ResultsTable.id_student == id_student)
    rows = req.all()
    pts = 0
    pts_total = 0
    for row in rows:
        if row.result in exam_results:
            pts += exam_results[row.result]
            pts_total += exam_results['отл']
        elif row.result in test_results:
            pts += test_results[row.result]
            pts_total += test_results['Зачёт']
        print(row.result)

    req = db.session.query(db.StudentsTable).filter(db.StudentsTable.id == id_student)
    student_name = req.first().name
    rate = (pts / pts_total) * 100
    print(student_name, 'rate:', round(rate,2))

def get_student_results(id_student: int) -> dict:
    student = db.session.query(db.StudentsTable).filter(db.StudentsTable.id == id_student).first()
    id_study = student.id_study
    semester = student.semester

    # Get subjects
    q = db.session.query(db.SubjectsTable)
    rows = q.filter(db.SubjectsTable.id_study == id_study, 
                    db.SubjectsTable.semester <= semester)
    subjects = rows.order_by(db.SubjectsTable.semester).all()
    
    student_results = dict()

    print(student.name, student.semester, 'семестр')
    # Get results
    for subject in subjects:
        q = db.session.query(db.ResultsTable).filter(db.ResultsTable.id_subject == subject.id)
        result = q.first().result
        print(subject.name, subject.semester, 'семестр', '|', 'оценка', result)

    return student_results


def subject_result(id_subject: int):
    subject = db.session.query(db.SubjectsTable).filter(db.SubjectsTable.id == id_subject).first()
    id_study = subject.id_study
    subject_semester = subject.semester

    print(subject.name, subject.semester, 'семестр')
    q = db.session.query(db.StudentsTable)
    rows = q.filter(db.StudentsTable.id_study == id_study, 
                        db.StudentsTable.semester == subject_semester)
    students = rows.all()
    for student in students:
        result_obj = db.session.query(db.ResultsTable).filter(db.ResultsTable.id_student == student.id).first()
        result = result_obj.result
        print(student.name, result)


######### CLI INTERFACE #########

# 1
# count top 10 and last 10 students
# 1 Ivan Ivanov Math rate: 100
# 2 Katya Denisova Biology rate: 90

# count study rate
# count rate: study + subject
# count rate: 

# count rate by 

# TEST 
# Programming with C
# id = 6254, id_study = 39, semester = 3

# TEST
# Student 1163, id_study 39, semester 3
# Student 1164, id_study 39, semester 7

# count_student_rate(1164)
get_student_results(1163)
# subject_result(1130)


