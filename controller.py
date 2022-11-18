"""
Controller gets user input from view, and return searching results

"""

import sys
import models

class SubjectsSearcher:
    """
        Studies name + id
        Subjects name + id
    """

    def __init__(self):
        self.studies_searched = [] 
        self.sheet_header = {}
        self.sheet = []

    def find_studies(self, search_str: str, trace=False):
        """
            this should return studies names with ids
            for using db api
        """
        search_title = search_str.title()
        search = f"%{search_title}%"
        studies = models.session.query(models.Studies) \
                                .filter(models.Studies.name.like(search)) \
                                .all()

        if trace:
            test_study = studies[0]
            splitted = test_study.name.split()
            code = splitted[0]
            name = " ".join(splitted[2:])
            study_dict = {'code': code, 'name': name, 'form':test_study.form}
            print(study_dict)

        self.studies_searched = tuple(
            {'name':study.name, 'form': study.form, 'id':study.id} for study in studies
        )

    def find_subjects(self, study_num: int):
        subjects = models.session.query(models.Subjects.name, 
                                        models.Subjects.semester, 
                                        models.Subjects.id) \
                                 .where(models.Subjects.id_study == study_num) \
                                 .order_by(models.Subjects.semester) \
                                 .all()
        result = [{'name': subj.name, 'semester': subj.semester, 'id':subj.id} for subj in subjects]

        self.subjects_searched = tuple(result)

    def study(self, index):
        return self.studies_searched[index]

    def studies_rows(self) -> tuple:
        return tuple(study['name'] + ' ' + study['form'] for study in self.studies_searched)

    def subjects_rows(self):
        return tuple(subj['name'] + ' ' + str(subj['semester']) for subj in self.subjects_searched)

    def get_sheet(self):
        
        pass


if __name__ == '__main__':

    studies_search_reqs = (
        'Физик',
        'Био',
        'Прикла',
        'Мар',
        'Экономика',
    )

    if 'test-studies' in sys.argv:
        searcher = SubjectsSearcher()

        searcher.find_studies(studies_search_reqs[1])
        
        print(searcher.studies_rows())
