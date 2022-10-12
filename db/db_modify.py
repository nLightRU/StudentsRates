import sys
import sqlite3
import random

database_path = 'university_results.db'

def get_studies(db_path) -> list:
    """
    Returns list of studies with id, name, degree 
    and how many students at this study
    """
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()

        res = cur.execute( 'SELECT Studies.id, Studies.name, Studies.degree, \
                            COUNT(Students.name) as number \
                            FROM Students JOIN Studies on Students.id_study = Studies.id \
                            GROUP BY Students.id_study '
                        )
        
        return res.fetchall()
    
def fill_semesters(db_path) -> None:
    studies = get_studies(db_path)

    with sqlite3.connect(db_path) as con:
        cur = con.cursor()  

        req_students_in_study = 'SELECT id, name, id_study FROM Students WHERE id_study = ?'
        req_max_semester = 'SELECT MAX(semester) FROM Subjects WHERE id_study = ?'
        req_add_semester = 'UPDATE Students SET semester = ? WHERE id = ?'
        
        for study in studies:
            study_id = study[0]
            semester_max = cur.execute(req_max_semester, (study_id,)).fetchone()[0]
            # print(study[1], semester_max)

            students = cur.execute(req_students_in_study, (study_id,)).fetchall()
            for student in students:
                semester = random.randint(1, semester_max)
                # print(student[1], semester)
                cur.execute(req_add_semester, (semester, student[0]))

        con.commit()

def fill_results(db_path):
    tests_results = {
        'Зачет': ('зачет','незачет',),
        'Экзамен': ('неуд','уд','хор','отл',),
        'Реферат': ('неуд','уд','хор','отл',),
        'Курсовая работа': ('неуд','уд','хор','отл',),
        'Зачет с оценкой': ('неуд','уд','хор','отл',),
        'Дифференцированный зачет': ('неуд','уд','хор','отл',),
        'Защита ВКР': ('неуд','уд','хор','отл',),
        'Контрольная работа': ('неуд','уд','хор','отл',),
        'Научный доклад': ('неуд','уд','хор','отл',),
        'ГЭК': ('неуд','уд','хор','отл',),
    }

    req_get_studies = 'SELECT id, name FROM Studies'
    req_get_students = 'SELECT id, name, semester FROM Students WHERE id_study = ?'
    req_get_subjects = 'SELECT id, name, semester, test FROM Subjects WHERE id_study = ? AND semester <= ?'
    req_insert_result = 'INSERT INTO Results(id_student, id_subject, result) VALUES(?,?,?)'

    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        
        studies = cur.execute(req_get_studies).fetchall()
        total_studies = len(studies)

        for study in studies:
            id_study = study[0]
            # trace study
            print('{} / {}'.format(id_study, total_studies))
            
            students = cur.execute(req_get_students, (id_study,)).fetchall()
            for student in students:
                semester = student[2]
                subjects = cur.execute(req_get_subjects, (id_study, semester)).fetchall()
                for subject in subjects:
                    if subject[3] in tests_results:
                        id_student = student[0]
                        id_subject = subject[0]

                        results = tests_results[subject[3]]
                        index = random.randint(0, len(results) - 1)
                        result = results[index]

                        cur.execute(req_insert_result, (id_student, id_subject, result))
            
        con.commit()

if __name__ == '__main__':
    if 'fill-semesters' in sys.argv:
        fill_semesters(database_path)
    elif 'fill-results' in sys.argv:
        fill_results(database_path)