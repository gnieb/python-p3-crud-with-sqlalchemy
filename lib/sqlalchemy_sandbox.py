#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    Index('index_name', 'name')

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default = datetime.now())

    def __repr__(self):
        return f"Student {self.id}: " \
        + f"{self.name}, " \
        + f"Grade {self.grade}"

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)


    Session = sessionmaker(bind=engine)
    session = Session()


    albert_einstein = Student(
        name = "Albert Einstein",
        email = "albert.einstein@zurich.edu",
        grade = 6,
        birthday = datetime(
        year=1879,
        month = 3,
        day=14
        ),
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )

    session.bulk_save_objects([albert_einstein, alan_turing])
    session.commit()

    # print(f"New student ID is {albert_einstein.id}.")
    # print(f"New student ID is {alan_turing.id}.")


    # students = session.query(Student)
    # print([student for student in students])

    ####  OR #####

    # students = session.query(Student).all()
    # print(students)


    #SORT BY NAME
    # names = session.query(Student.name).all()
    # print(names)

    #SORT BY NAME AND ORDER BY NAME

    # students_by_name = session.query(
    #     Student.name).order_by(
    #     Student.name).all()
    # print(students_by_name)

    #SORT IN DESC ORDER BY GRADE

    # students_by_grade_desc = session.query(
    #     Student.name, Student.grade).order_by(
    #     desc(Student.grade)).all()
    # print(students_by_grade_desc)

    #LIMIT  RESULT SET TO 'X' AMOUNT OF RECORDS

    # oldest_student = session.query(
    #     Student.name, Student.birthday).order_by(
    #     desc(Student.grade)).limit(1).all()

    # print(oldest_student)

    #### OR USE first() ###

    # oldest_student = session.query(
    #         Student.name, Student.birthday).order_by(
    #         desc(Student.grade)).first()
    # print(oldest_student)
    
# USING FUNC

    # student_count = session.query(func.count(Student.id)).first()
    # print(student_count)


    # FILTERING

    # query = session.query(Student).filter(Student.name.like('%Alan%'),
    #     Student.grade ==11).all()
    
    
    # for record in query:
    #     print(record.name)

    # UPDATING DATA
# The simplest is to use Python to modify objects directly and then commit those changes through the session. For instance, let's say that a new school year is starting and our students all need to be moved up a grade:

    # for student in session.query(Student):
    #     student.grade += 1

    # session.commit()

    # print([(student.name, student.grade) for student in session.query(Student)])

    #OR BETTER YET, use the UPDATE() METHOD TO UPDATE RECORDS
    
    # session.query(Student).update({
    #     Student.grade: Student.grade + 1
    # })
    # print([(
    #     student.name,
    #     student.grade
    # ) for student in session.query(Student)])

    #DELETING DATA

    # query = session.query(
    #     Student).filter(
    #         Student.name == "Albert Einstein")        

    # # retrieve first matching record as object
    # albert_einstein = query.first()

    # # delete record
    # session.delete(albert_einstein)
    # session.commit()

    # # try to retrieve deleted record
    # albert_einstein = query.first()

    # print(albert_einstein)

    #### OR, If you don't have a single object ready for deletion but you know the criteria for deletion, you can call the delete() method from your query instead:######

     # create session, student objects

    query = session.query(
        Student).filter(
            Student.name == "Albert Einstein")

    query.delete()

    albert_einstein = query.first()

    print(albert_einstein)

    # CAREFUL: This strategy will delete all records returned by your query, so be careful!