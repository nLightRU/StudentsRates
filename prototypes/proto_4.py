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


######### CLI INTERFACE #########

# 1
# count top 10 and last 10 students
# 1 Ivan Ivanov Math rate: 100
# 2 Katya Denisova Biology rate: 90

# count study rate
# count rate: study + subject
# count rate: 

# count rate by 

count_student_rate(1171)


