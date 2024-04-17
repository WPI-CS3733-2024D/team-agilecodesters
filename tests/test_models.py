import warnings

warnings.filterwarnings("ignore")

from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.Model.models import Student, Faculty, Major, ResearchPosition, Applications
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


class TestModels(unittest.TestCase):
    # from student-app
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    # from student-app
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_apply_for_research(self):
        test_major = Major(name="Computer Science")
        db.session.add(test_major)
        db.session.commit()

        student = Student(
            major=test_major.id,
            GPA=3.5,
            graduationdate=datetime.now() + timedelta(days=365 * 3),  # 3 years from now
        )

        student.set_password("securepassword")  # Setting a password if necessary
        db.session.add(student)
        db.session.commit()

        research_position = ResearchPosition(
            title="ML/AI Research",
        )
        db.session.add(research_position)
        db.session.commit()

        # Apply to the research position
        application = Applications(
            studentID=student.id,
            position=research_position.id,
            # Assume other required fields are set up here
        )
        db.session.add(application)
        db.session.commit()

        # Test if the student has applied to the position
        self.assertTrue(student.has_applied_to_position(research_position.id))
