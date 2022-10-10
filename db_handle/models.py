from sqlalchemy.orm import declarative_base

from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

class Study(Base):
    __tablename__ = 'Studies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    degree = Column(String)
    form = Column(String)


class Subject(Base):
    __tablename__ = 'Subjects'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    id_study = Column(Integer, ForeignKey('Studies.id'))
    semester = Column(Integer)
    test = Column(String)

    def __repr__(self) -> str:
        return '<Subject(name=%s, id_study=%d, test=%s)>' % (self.name, self.id_study, self.test)

class Student(Base):
    __tablename__ = 'Students'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    id_study = Column(Integer, ForeignKey('Studies.id'))

    def __repr__(self) -> str:
        return '<Student(name=%s, id_study=%d)>' % (self.name, self.id_study)