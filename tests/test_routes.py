import pytest
from app import create_app, db
from app.Model.models import (
    Faculty,
    Student,
    User,
    ResearchPosition,
    Applications,
    ResearchField,
    ProgrammingLanguage,
    Department,
    Major,
)
from app.Controller.routes import login_required
from config import Config


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SECRET_KEY = "bad-bad-key"
    WTF_CSRF_ENABLED = False
    DEBUG = True
    TESTING = True


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app(config_class=TestConfig)
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()


def init_database(request, test_client, init_database):

    db.create_all()
    # Insert user data
    if Department.query.count() == 0:
        departments = [
            {"name": "Computer Science"},
            {"name": "Engineering"},
            {"name": "Gaming"},
            {"name": "Business"},
            {"name": "Hard Sciences"},
        ]
        for department in departments:
            new_department = Department(name=department["name"])
            db.session.add(new_department)
        db.session.commit()
    if Major.query.count() == 0:
        majors = [
            {"name": "Computer Science", "dname": "Computer Science"},
            {"name": "Robotics Engineering", "dname": "Engineering"},
            {"name": "Electrical and Computer Engineering", "dname": "Engineering"},
            {"name": "Mechanical Engineering", "dname": "Engineering"},
            {"name": "Chemical Engineering", "dname": "Engineering"},
            {"name": "Game ing", "dname": "Game ing"},
            {"name": "Coloring", "dname": "Business"},
            {"name": "Biology", "dname": "Hard Sciences"},
            {"name": "Chemistry", "dname": "Hard Sciences"},
            {"name": "Biochemistry", "dname": "Hard Sciences"},
            {"name": "Physics", "dname": "Hard Sciences"},
            {"name": "Biochemicalphysics", "dname": "Hard Sciences"},
        ]
        for major in majors:
            with db.session.no_autoflush:
                department = Department.query.filter_by(name=major["dname"]).first()
                if department:
                    new_major = Major(name=major["name"], department=department.id)
                    db.session.add(new_major)
        db.session.commit()

    if ProgrammingLanguage.query.count() == 0:
        languages = [
            "Python",
            "Java",
            "JavaScript",
            "C",
            "C++",
            "C#",
            "Ruby",
            "Swift",
            "Go",
            "PHP",
            "Kotlin",
        ]
        for lang in languages:
            new_lang = ProgrammingLanguage(title=lang)
            db.session.add(new_lang)
        db.session.commit()

    if ResearchField.query.count() == 0:
        fields = [
            "Artificial Intelligence",
            "Quantum Computing",
            "Machine Learning",
            "Ending the World",
            "Robotics",
            "Neural Networks",
            "Cybersecurity",
            "Biotechnology",
            "Space Exploration",
            "Becoming Iron Man",
            "Nanotechnology",
            "Augmented Reality",
            "Virtual Reality",
        ]
        for field in fields:
            new_field = ResearchField(title=field)
            db.session.add(new_field)
            db.session.commit()

    db.drop_all()


def test_index(request, test_client, init_database):
    response = test_client.get("/index", follow_redirects=True)
    test_client.post(
        "/login",
        data={"username": "JamesB", "password": "19256#"},
        follow_redirects=True,
    )

    test_client.get("/index", follow_redirects=True)
    assert response.status_code == 200
    assert b"All Available Positions" in response.data


def test_apply_for_position(request, test_client, init_database):
    # Create a student and a research position instance
    new_student = Student(username="carl100", email="carl100@outlook.com")
    new_student.set_password("carl19$tyu")  # Set the password
    new_position = ResearchPosition(title="Deep Learning Research")

    db.session.add(new_student)
    db.session.add(new_position)
    db.session.commit()

    position_id = new_position.id

    login_response = test_client.post(
        "/login",
        data={
            "username": new_student.username,
            "password": "carl19$tyu",  # Use the correct password set above
        },
        follow_redirects=True,
    )
    assert login_response.status_code == 200

    apply_response = test_client.post(
        f"/apply/{position_id}",
        data={
            "statement_of_interest": "I am very interested in this position ...",
            "reference_name": "Prof. Zoe David",
            "reference_email": "ProfZoe@gmail.com",
        },
        follow_redirects=True,
    )
    assert apply_response.status_code == 200

    application = Applications.query.filter_by(
        studentID=new_student.id, position=position_id
    ).first()

    assert application is not None
    assert (
        application.statement_of_interest == "I am very interested in this position ..."
    )
    assert application.referenceName == "Prof. Zoe David"
    assert application.referenceEmail == "ProfZoe@gmail.com"


def test_invalidlogin(request, test_client, init_database):
    response = test_client.post(
        "/login",
        data=dict(username="Kenneth", password="k12bostW$", remember_me=False),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data
