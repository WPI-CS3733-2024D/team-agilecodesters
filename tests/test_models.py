import warnings
warnings.filterwarnings("ignore")
import os
basedir = os.path.abspath(os.path.dirname(__file__))

from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.Model.models import User, Faculty, Student, ResearchPosition, Applications
from config import Config
from unittest.mock import patch

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ROOT_PATH = '..//'+basedir
    

class TestModels(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        student = Student(username='Joshua3', email='joshy34.adam1@gmail.edu')
        student.set_password('PASSWORDX')
        self.assertFalse(student.check_password('PAssWordX'))
        self.assertTrue(student.check_password('PASSWORDX'))
        self.assertFalse(student.check_password('passing_wrd'))

        faculty = Faculty(username='Joshua3', email='joshy34.adam1@gmail.edu')
        faculty.set_password('learn100josh')
        self.assertFalse(faculty.check_password('LEArn100jOSh'))
        self.assertTrue(faculty.check_password('learn100josh'))
        self.assertFalse(faculty.check_password('passing_wrd'))
    
    def test_studentLogin(self):
        student1 = Student(username = 'DanielB',
                           firstname = 'Dan', lastname = "Adams", email='dan100@gmail.edu',
                           phone_number = '1234567899', graduationdate = datetime.utcnow(), 
                           GPA = 3.5)
        
        student1.set_password("1234passtest")

        db.session.add(student1)
        db.session.commit()
        
        # get student from database
        get_student = Student.query.filter_by(username='DanielB').first()

        # check if student is in database
        self.assertIsNotNone(get_student, "Student should be in the database")

        self.assertEqual(get_student.username, student1.username)
        self.assertFalse(student1.check_password('1234PASStest'))
        self.assertTrue(student1.check_password('1234passtest'))
    
    def test_facultyLogin(self):
        faculty1 = Faculty(username = 'George_W',
                           firstname = 'Dan', lastname = "Adams", email='dan100@gmail.edu',
                           phone_number = '1234567899', researchAreas = "Computer Science", department = "CS Department" 
                          )
        
        faculty1.set_password("faculty100")

        db.session.add(faculty1)
        db.session.commit()
        
        # get student from database
        get_professor = Faculty.query.filter_by(username='George_W').first()

        # check if student is in database
        self.assertIsNotNone(get_professor, "Student should be in the database")

        self.assertEqual(get_professor.username, faculty1.username)
        self.assertFalse(faculty1.check_password('faculty101'))
        self.assertTrue(faculty1.check_password('faculty100'))
    
 
    def test_has_applied_to_position(self):

        student = Student(username='Amin100', email='sAmin@example.com')
        db.session.add(student)

        applied_position = ResearchPosition(title='AI research', description = "some description")
        db.session.add(applied_position)
        db.session.commit()

        # student applies to a position
        application = Applications(studentID=student.id, position=applied_position.id)
        db.session.add(application)
        db.session.commit()

        self.assertTrue(student.has_applied_to_position(applied_position))

        # Check with a position the student has not applied to
        unapplied_position = ResearchPosition(title='unapplied Position')
        db.session.add(unapplied_position)
        db.session.commit()

        self.assertFalse(student.has_applied_to_position(unapplied_position))


# Run the tests
if __name__ == '__main__':
    unittest.main(verbosity=2) # get more information on which tests are passing/failing






