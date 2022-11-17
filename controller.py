"""
Controller gets user input from view, and return searching results

"""

import sys
import models

class SubjectsSearcher:
    def __init__(self):
        self.studies_searched = [] 
        self.sheet_header = {}
        self.sheet = []

    def find_studies(self, search_str: str, trace=False):
        """
            this should return studies names with ids
            for using db api
        """
        search = f"%{search_str}%"
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

        self.studies_searched = [
            {'name':study.name, 'form': study.form, 'id':study.id} for study in studies
        ]

    def find_subjects(self, study_num: int):
        self.subjects_searched = models.get_academic_plan(self.studies_searched[study_num])

    def studies_rows(self) -> tuple:
        return tuple(study['name'] + ' ' + study['form'] for study in self.studies_searched)



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
