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
    __table_args__= (
        PrimaryKeyConstraint(
            'id',
            name = 'id_pk'),
        UniqueConstraint(
            'email',
            name='unique_email'),
        CheckConstraint(
            'grade BETWEEN 1 AND 12',
            name = 'grade_between_1_and_12'
        )
    )
    Index('index_name', 'name')

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String())
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

    def __repr__(self):
        return f"Student {self.id}" \
              +f"{self.name}," \
              +f"Grade {self.grade}"

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    session = Session()



if __name__ == '__main__':

    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        ),
    )

    alan_turing = Student(
        name='Alan Turing',
        email='alan.com',
        grade=11,
        birthday=datetime(
            year = 1912,
            month = 6,
            day = 23,
        ),
    )

    session.bulk_save_objects([albert_einstein, alan_turing])
    session.commit()

    students = session.query(Student).all()

    print(students)
       # print([student for student in students])

    # print(f"New student ID is {albert_einstein.id}.")
    # print(f"New student ID is {alan_turing.id}.")


    # session.add(albert_einstein)
    # session.commit()

    # print(f"New student ID is {albert_einstein.id}.")

    #Selecting Only Certain Columns-------------

    names = [name for name in session.query(Student.name)]
    print(names)

    
    #Ordering-------------

    students_by_name = [student for student in session.query(
            Student.name).order_by(
            Student.name)]

    print(students_by_name)
    # => [('Alan Turing',), ('Albert Einstein',)]



    #To sort results in descending order-------------


    students_by_grade_desc = [student for student in session.query(
            Student.name, Student.grade).order_by(
            desc(Student.grade))]
    
    print(students_by_grade_desc)
    # => [('Alan Turing', 11), ('Albert Einstein', 6)]


    #Limiting-------------To limit your result set to the first x records, you can use the limit() method:


    oldest_student = [student for student in session.query(
        Student.name, Student.birthday).order_by(
        desc(Student.grade)).limit(1)]
    
    print(oldest_student)
    # => [('Alan Turing', datetime.datetime(1912, 6, 23, 0, 0))]



    #The first() method is a quick and easy way to execute a limit(1) statement and does-------
    
    oldest_student = session.query(
        Student.name, Student.birthday).order_by(
            desc(Student.grade)).first()
    
    print(oldest_student)
    # => ('Alan Turing', datetime.datetime(1912, 6, 23, 0, 0))



    #func--------------

    student_count = session.query(func.count(Student.id)).first()

    print(student_count)

    # => (2,)

    #Filtering--------------Retrieving specific records requires use of the filter()

    query = session.query(Student).filter(Student.name.like('%Alan%'),
        Student.grade == 11)

    for record in query:
        print(record.name)

    # => Alan Turing



    #Updating Data--------------

    for student in session.query(Student):
        student.grade += 1

        session.commit()

        print([(student.name,
        student.grade) for student in session.query(Student)])

    # => [('Albert Einstein', 7), ('Alan Turing', 12)]

    #The update() method allows us to update records
    # without creating objects beforehand.
    # Here's how we would carry out the same statement with update():

        session.query(Student).update({
        Student.grade: Student.grade + 1
    })

    print([(
        student.name,
        student.grade
    ) for student in session.query(Student)])

# => [('Albert Einstein', 7), ('Alan Turing', 12)]



#Deleting Data--------------

    query = session.query(
            Student).filter(
                Student.name == "Albert Einstein")

    # retrieve first matching record as object
    albert_einstein = query.first()
    
     # delete record
    session.delete(albert_einstein)
    session.commit()

    # try to retrieve deleted record
    albert_einstein = query.first()

    print(albert_einstein)

    # => None

    #If you don't have a single object ready for deletion
    # but you know the criteria for deletion,
    # you can call the delete() method 
    # from your query instead:

    query = session.query(
        Student).filter(
            Student.name == "Albert Einstein")

    query.delete()

    albert_einstein = query.first()

    print(albert_einstein)

# => None