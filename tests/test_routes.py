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
from datetime import datetime, timedelta
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


@pytest.fixture
def init_database():
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

    yield  # this is where the testing happens!

    db.drop_all()



def new_student(
    uname, uemail, passwd, firstname, lastname, major, GPA, grad_date, phone_number
):
    """Creates a new student instance

    Args:
        uname (): username
        uemail (): email
        passwd (): password (will be hashed before storing in the database)
        firstname (): first name
        lastname (): last name
        major (): major
        GPA (): GPA
        grad_date (): graduation date
        phone_number (): phone number

    Returns:
        Student: a new student instance
    """
    student = Student(
        username=uname,
        email=uemail,
        firstname=firstname,
        lastname=lastname,
        major=major,
        GPA=GPA,
        graduationdate=grad_date,
        phone_number=phone_number,
        user_type="Student",
    )

    student.set_password(passwd)
    return student


def new_faculty(
    uname, uemail, passwd, firstname, lastname, research_areas, depart, phone_number
):
    """Creates a new faculty instance

    Args:
        uname ():
        uemail ():
        passwd ():
        firstname ():
        lastname ():
        research_areas ():
        depart ():
        phone_number ():

    Returns:
        Faculty: a new faculty instance
    """
    a_faculty = Faculty(
        username=uname,
        email=uemail,
        firstname=firstname,
        lastname=lastname,
        researchAreas=research_areas,
        department=depart,
        phone_number=phone_number,
        user_type="Student",
    )

    a_faculty.set_password(passwd)
    return a_faculty


def test_index(request, test_client, init_database):
    """Tests index route
        - tests student and faculty being added
        - tests student login
        - tests faculty login
    Args:
        request ():
        test_client ():
        init_database ():
    """
    student = new_student(
        uname="jonB",
        uemail="jon@gmail.com",
        passwd="123",
        firstname="Jon",
        lastname="Adams",
        major="CS",
        GPA=3.8,
        grad_date=None,
        phone_number="8888888888",
    )
    db.session.add(student)
    db.session.commit()

    faculty = new_faculty(
        uname="Brandon_81",
        uemail="Brandon_81@outlook.com",
        passwd="100successtest",
        firstname="Brandon",
        lastname="Welton",
        research_areas="Biology",
        depart="Biomedical department",
        phone_number="4444444444",
    )
    db.session.add(faculty)
    db.session.commit()

    thestud = Student.query.filter_by(username="jonB", email="jon@gmail.com")
    theprof = Faculty.query.filter_by(
        username="Brandon_81", email="Brandon_81@outlook.com"
    )
    assert thestud is not None
    response = test_client.post(
        "/login",
        data=dict(username="jonB", password="123", remember_me=False),
        follow_redirects=True,
    )
    assert response.status_code == 200

    response = test_client.post(
        "/login",
        data=dict(username="Brandon_81", password="100successtest", remember_me=False),
        follow_redirects=True,
    )

    assert response.status_code == 200

    response = test_client.get("/index", follow_redirects=True)
    # test_client.post(
    #     "/login",
    #     data={"username": "JamesB", "password": "19256#"},
    #     follow_redirects=True,
    # )

    # test_client.get("/index", follow_redirects=True)
    assert response.status_code == 200
    assert b"All Available Positions" in response.data


def test_student_register_apply(request, test_client, init_database):
    """Tests student registration and application submission
        - register/student
        - register/faculty
        - login (faculty)
        - logout (faculty)
        - login (student)
        - add position
        - apply

    Args:
        request ():
        test_client ():
        init_database ():
    """
    """Tests student registration

    Args:
        request (): 
        test_client (): 
        init_database (): 
    """

    # Create a student and a research position instance
    thestudent = new_student(
        uname="jonB",
        uemail="jon@gmail.com",
        passwd="123",
        firstname="Jon",
        lastname="Adams",
        major="CS",
        GPA=3.8,
        grad_date=None,
        phone_number="8888888888",
    )

    thefaculty = new_faculty(
        uname="cew",
        uemail="cew@wpi.edu",
        passwd="123",
        firstname="Craig",
        lastname="Wills",
        research_areas="Computer Networks",
        depart="Computer Science",
        phone_number="8888888888",
    )

    db.session.add(thestudent)
    db.session.add(thefaculty)
    db.session.commit()

    # Test post request for both

    thestudent_registers = test_client.post(
        "/register/student",
        data=dict(
            username="jonB",
            password="123",
            email="jon@gmail.com",
            firstname="Jon",
            lastname="Adams",
            major="CS",
            GPA=3.8,
            grad_date=None,
            phone_number="8888888888",
            remember_me=False,
        ),
        follow_redirects=True,
    )
    assert thestudent is not None
    assert thestudent_registers.status_code == 200

    thefaculty_registers = test_client.post(
        "/register/faculty",
        data=dict(
            username="cew",
            password="123",
            email="cew@wpi.edu",
            firstname="Craig",
            lastname="Wills",
            research_areas="Computer Networks",
            department="Computer Science",
            phone_number="8888888888",
            remember_me=False,
        ),
        follow_redirects=True,
    )
    assert thefaculty is not None
    assert thefaculty_registers.status_code == 200

    # Retrieve the student and faculty from the database, double check they're there before moving on
    retrieved_student_id = (
        Student.query.filter_by(username="jonB", email="jon@gmail.com").first().id
    )
    retrieved_faculty_id = (
        Faculty.query.filter_by(username="cew", email="cew@wpi.edu").first().id
    )

    # Assert that the retrieved student and faculty are not None
    assert retrieved_student_id
    assert retrieved_faculty_id

    # Log in the student to apply for the position
    response = test_client.post(
        "/login",
        data=dict(username="jonB", password="123", remember_me=False),
        follow_redirects=True,
    )
    assert response.status_code == 200
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=10)

    new_position = ResearchPosition(
        title="Deep Learning Research",
        # Specifies the lowest desired GPA
        wantedGPA=3.0,
        description="Study Physics 101",
        researchGoals="To learn more about physics ... ",
        startDate=start_date,
        endDate=end_date,
        timeCommitment=3,
        faculty=retrieved_faculty_id,
    )
    db.session.add(new_position)
    db.session.commit()

    assert new_position is not None

    position = ResearchPosition.query.filter_by(
        title="Deep Learning Research",
        # Specifies the lowest desired GPA
        wantedGPA=3.0,
        description="Study Physics 101",
        researchGoals="To learn more about physics ... ",
        startDate=start_date,
        endDate=end_date,
        timeCommitment=3,
    ).first()

    assert position is not None

    position_id = position.id
    assert position_id is not None

    # Apply for the position
    application = Applications(
        studentID=retrieved_student_id,
        position=position_id,
        statement_of_interest="I am very interested in this position ...",
        referenceName="Johnson David",
        referenceEmail="ProfZoe@gmail.com",
    )
    db.session.add(application)
    db.session.commit()

    apply_response = test_client.post(
        f"/apply/{position_id}",
        data=dict(
            studentID=retrieved_student_id,
            position=position_id,
            statement_of_interest="I am very interested in this position ...",
            referenceName="Johnson David",
            referenceEmail="ProfZoe@gmail.com",
        ),
        follow_redirects=True,
    )

    response = test_client.get("/index", follow_redirects=True)

    assert apply_response.status_code == 200

    # print all the applications
    applications = Applications.query.all()
    for application in applications:
        print("APP!")
        print(application)

    application = Applications.query.filter_by(
        studentID=retrieved_student_id, position=position_id
    ).first()
    assert application is not None, "Application was not created in the database"

    # assert application is not None
    assert (
        application.statement_of_interest == "I am very interested in this position ..."
    )
    assert application.referenceName == "Johnson David"
    assert application.referenceEmail == "ProfZoe@gmail.com"


# def test_faculty_create_position(request, test_client, init_database):
#     """Tests faculty making a position
#         - register/faculty
#         - login (faculty)
#         - add position
#     Args:
#         request ():
#         test_client ():
#         init_database ():
#     """
#     thefaculty = new_faculty(
#         uname="cew",
#         uemail="cew@wpi.edu",
#         passwd="123",
#         firstname="Craig",
#         lastname="Wills",
#         research_areas="Computer Networks",
#         depart="Computer Science",
#         phone_number="8888888888",
#     )
#
#     db.session.add(thefaculty)
#     db.session.commit()
#
#     thefaculty_registers = test_client.post(
#         "/register/faculty",
#         data=dict(
#             username="cew",
#             password="123",
#             email="cew@wpi.edu",
#             firstname="Craig",
#             lastname="Wills",
#             research_areas="Computer Networks",
#             department="Computer Science",
#             phone_number="8888888888",
#             remember_me=False,
#         ),
#         follow_redirects=True,
#     )
#
#     assert thefaculty is not None
#     assert thefaculty_registers.status_code == 200
#
#     faculty_id = Faculty.query.filter_by(username="cew", email="cew@wpi.edu").first().id
#     assert faculty_id is not None
#
#     response = test_client.post(
#         "/login",
#         data=dict(username="cew", password="123", remember_me=False),
#         follow_redirects=True,
#     )
#     assert response.status_code == 200
#
#
#     start_date = datetime.utcnow()
#     end_date = start_date + timedelta(days=10)
#
#     new_position = ResearchPosition(
#         title="Deep Learning Research",
#         # Specifies the lowest desired GPA
#         wantedGPA=3.0,
#         description="Study Physics 101",
#         researchGoals="Study Physics ...",
#         startDate=start_date,
#         endDate=end_date,
#         timeCommitment=3,
#         faculty=faculty_id,
#     )
#     db.session.add(new_position)
#     db.session.commit()
#
#     assert new_position is not None
#
#     position = ResearchPosition.query.filter_by(
#         title="🅱️eep 🅱️earning 🅱️esearch",
#         # Specifies the lowest desired GPA
#         wantedGPA=3.0,
#         description="🅱️tudy 🅱️hysics 🅱️01",
#         researchGoals="🅱️tudy 🅱️hysics ...",
#         startDate=start_date,
#         endDate=end_date,
#         timeCommitment=3,
#     ).first()
#
#     assert position is not None
#
#     position_response = test_client.post(
#         "/create_position",
#         data=dict(
#             title="🅱️eep 🅱️earning 🅱️esearch",
#             # Specifies the lowest desired GPA
#             wantedGPA=3.0,
#             description="🅱️tudy 🅱️hysics 🅱️01",
#             researchGoals="🅱️tudy 🅱️physics ...",
#             startDate=start_date,
#             endDate=end_date,
#             timeCommitment=3,
#             faculty=faculty_id,
#         ),
#         follow_redirects=True,
#     )
#     assert position_response.status_code == 200
#     assert "🅱️tudy 🅱️hysics 🅱️01" in position_response.data
#

def test_studentinvalidlogin(request, test_client, init_database):
    """Tests invalid student login
        - tests if a student with invalid username and password logs in
    Args:
        request ():
        test_client ():
        init_database ():
    """
    student = new_student(
        uname="jonB",
        uemail="jon@gmail.com",
        passwd="123",
        firstname="Jon",
        lastname="Adams",
        major="CS",
        GPA=3.8,
        grad_date=None,
        phone_number="8888888888",
    )
    student.set_password("carl19$tyu")  # Set the password

    db.session.add(student)
    db.session.commit()

    response = test_client.post(
        "/login",
        data=dict(username="Kenneth", password="k12bostW$", remember_me=False),
        follow_redirects=True,
    )
    assert response.status_code == 200 or response.status_code == 302
    if response.status_code == 302:
        assert (
            b"Invalid username or password" in response.data
        ), "Error message was not found"


def test_facultyinvalidlogin(request, test_client, init_database):
    """Tests invalid faculty login

    Args:
        request ():
        test_client ():
        init_database ():
    """
    faculty = new_faculty(
        uname="jonB",
        uemail="jon@gmail.com",
        passwd="1745hj",
        firstname="Jon",
        lastname="Adams",
        research_areas="Artificial Intelligence",
        depart="Computer Science",
        phone_number="8888888888",
    )

    db.session.add(faculty)
    db.session.commit()

    response = test_client.post(
        "/login",
        data=dict(username="Adam", password="jf43gfj$", remember_me=False),
        follow_redirects=True,
    )
    assert response.status_code == 200 or response.status_code == 302
    if response.status_code == 302:
        assert (
            b"Invalid username or password" in response.data
        ), "Error message was not found"


def test_login_logout_faculty(request, test_client, init_database):
    """Tests valid faculty login

    Args:
        request ():
        test_client ():
        init_database ():
    """
    faculty = new_faculty(
        uname="JasonR_Xl",
        uemail="jon@gmail.com",
        passwd="1745hj",
        firstname="Jon",
        lastname="Adams",
        research_areas="Artificial Intelligence",
        depart="Computer Science",
        phone_number="8888888888",
    )
    db.session.add(faculty)
    db.session.commit()

    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' form is submitted (POST) with correct credentials
    THEN check that the response is valid and login is succesfull 
    """
    response = test_client.post(
        "/login",
        data=dict(username="JasonR_Xl", password="happisc89", remember_me=False),
        follow_redirects=True,
    )

    assert response.status_code == 200 or response.status_code == 302
    if response.status_code == 302:
        assert (
            b"Invalid username or password" in response.data
        ), "Error message was not found"

    # response = test_client.get('/logout',
    #                       follow_redirects = True)
    # assert response.status_code == 200
    # assert b"Sign In" in response.data
