from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


studentFields = db.Table(
    "studentFields",
    db.Column("student_id", db.Integer, db.ForeignKey("student.id")),
    db.Column("field_id", db.Integer, db.ForeignKey("researchfields.id")),
)


# A super class representing a generic user
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wpi_id = db.Column(db.Integer, unique=True)
    username = db.Column(db.String(20), unique=True)
    # A hash of the password, kept as a hash for security
    password_hash = db.Column(db.String(20))
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    email = db.Column(db.String(20), unique=True)
    phone = db.Column(db.String(10))


# A sub-class of User, representing a student user
class Student(User):
    major = db.Column(db.String(20))
    GPA = db.Column(db.Float)
    graduationdate = db.Column(db.String(20))
    user_type = db.Column(db.String(20))
    # Topics of interest coincides with research Areas in faculty
    topics_of_interest = db.relationship(
        "ResearchFields",
        secondary=studentFields,
        primaryjoin=(studentFields.c.student_id == id),
        backref=db.backref("studentFields", lazy="dynamic"),
        lazy="dynamic",
    )
    appliedPositions = db.relationship(
        "Applications", back_populates="student_enrolled"
    )

    def __repr__(self):
        return "<Student {} - {} - {}>".format(self.id, self.firstname, self.lastname)

    # By using set_password, we don't store the user's password, increasing security
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# A sub-class of User, representing the faculty users
class Faculty(User):
    # Research Areas coincide with Topics of Interest in the Student model
    researchAreas = db.Column(db.String(150))
    department = db.Column(db.String(20), db.ForeignKey("department.name"))
    user_type = db.Column(db.String(20))

    def __repr__(self):
        return "<Faculty {} - {}, {}. {} Deparment>".format(
            self.id, self.lastname, self.firstname, self.department
        )

    # By using set_password, we don't store the user's password, increasing security
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Department(db.Model):
    """
    Represents departments in university that professors are associated with
    Attributes: 
        id: Integer, primary key
        name: String, unique 
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __repr__(self):
        return f"<Department: {self.name} [id {self.id}]>"


# Represents the research fields that the website can handle
class ResearchFields(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    attachedPosition = db.relationship("Position_Fields", back_populates="fields")

    student_interested = db.relationship(
        "Student",
        secondary=studentFields,
        primaryjoin=(studentFields.c.field_id == id),
        backref=db.backref("studentFields", lazy="dynamic"),
        lazy="dynamic",
    )


# Represents the posted research positions
class ResearchPosition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True)
    # Specifies the lowest desired GPA
    wantedGPA = db.Column(db.Float)
    languages = db.Column(db.String(150))
    description = db.Column(db.String(1500))
    researchGoals = db.Column(db.String(1500))
    startDate = db.Column(db.DateTime)
    endDate = db.Column(db.DateTime)
    # faculty_name = db.Column(db.String(20))
    # faculty_email = db.Column(db.String(20), db.ForeignKey("faculty.email"))
    faculty = db.Column(db.Integer, db.ForeignKey("faculty.id"))

    students_application = db.relationship(
        "Student_App", back_populates="enrolled_position"
    )
    researchFields = db.relationship("Position_Fields", back_populates="position")

    def __repr__(self):
        return "<Research Position: {} -- Description: {}>".format(
            self.title, self.description
        )


# A relationship table relation research positions and the fields they pertain to
class PositionField(db.Model):
    pos_ID = db.Column(
        db.Integer, db.ForeignKey("research_position.id"), primary_key=True
    )
    field_ID = db.Column(
        db.Integer, db.ForeignKey("research_fields.id"), primary_key=True
    )

    # Represent relationships to Positions and ResearchFields respectively
    position = db.relationship("Research_Position")
    fields = db.relationship("Research_Fields")


# A relationship table relating students to positions they have applied to
class Applications(db.Model):
    studentID = db.Column(db.Integer, db.ForeignKey("student.wpi_id"), primary_key=True)
    position = db.Column(
        db.Integer, db.ForeignKey("research_position.id"), primary_key=True
    )

    # Represent relationships to student and ResearchPosition respectively
    student_erolled = db.relationship("Student")
    enrolled_position = db.relationship("Research_Position")

    # statement of interest
    statement_of_interest = db.Column(db.String(1200))

    # TODO (listed by Myrrh): reference fields

    def __repr__(self):
        return "<studentID: {} --- position: {}>".format(self.studentID, self.position)


@login.user_loader
def load_user(wpi_id):
    return Student.query.get(int(wpi_id))
