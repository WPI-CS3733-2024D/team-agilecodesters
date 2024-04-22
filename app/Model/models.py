from enum import Enum
from sqlalchemy import ForeignKey
from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# Table linking students to research fields
studentFields = db.Table(
    "studentFields",
    db.Column("student_id", db.Integer, db.ForeignKey("student.id")),
    db.Column("field_id", db.Integer, db.ForeignKey("research_field.id")),
)
# Table linking students to programming languages
studentLanguages = db.Table(
    "studentLanguages",
    db.Column("student_id", db.Integer, db.ForeignKey("student.id")),
    db.Column("language_id", db.Integer, db.ForeignKey("programming_language.id")),
)
# Table linking positions to programming languages
positionLanguages = db.Table(
    "positionLanguages",
    db.Column("position_id", db.Integer, db.ForeignKey("research_position.id")),
    db.Column("language_id", db.Integer, db.ForeignKey("programming_language.id")),
)

facultyInterests = db.Table(
    "facultyInterests",
    db.Column("faculty_id", db.Integer, db.ForeignKey("faculty.id")),
    db.Column("field_id", db.Integer, db.ForeignKey("research_field.id")),
)


# TODO: cite sources for inheritance
# Sources for inheritance:
# - https://github.com/briangreunke/sqlalchemy-inheritance/blob/master/inherit.py
# - https://stackoverflow.com/questions/1337095/sqlalchemy-inheritance


# Enum repreenting type of user, for consistency
class UserType(Enum):
    User = "user"
    Student = "student"
    Faculty = "faculty"


class User(db.Model, UserMixin):
    """
    Superclass for all users. Each user is either a student or faculty
    Attributes:
        __tablename__: String for inheritance
        id: Integer, primary key
        username: String, unique, max 20 characters
        password_hash: String, max 20 characters
        firstname: String, max 20 characters
        lastname: String, max 20 characters
        email: String, unique, max 20 characters
        phone: String, max 10 characters
        __mapper_args__: Polymorphic identity for inheritance
    """

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    # wpi_id = db.Column(db.Integer, unique=True)
    username = db.Column(db.String(20), unique=True)
    # A hash of the password, kept as a hash for security
    password_hash = db.Column(db.String(20))
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    email = db.Column(db.String(20), unique=True)
    phone_number = db.Column(db.String(10))

    __mapper_args__ = {
        "polymorphic_identity": UserType.User,
    }


# A sub-class of User, representing a student user
class Student(User):
    """
    Represents a student user, inheriting from User
    Attributes:
        __tablename__: String for inheritance
        id: Foreign key to User, primary key
        major: foreign key to Major
        GPA: Float
        graduationdate: String, max 20 characters
        user_type: String, max 20 characters
        topics_of_interest: Many-to-many relationship with ResearchField
        appliedPositions: One-to-many relationship with Applications
        __mapper_args__: Polymorphic identity for inheritance

    """

    __tablename__ = "student"
    id = db.Column(None, ForeignKey("user.id"), primary_key=True)

    major = db.Column(db.Integer, db.ForeignKey("major.id"))
    GPA = db.Column(db.Float)
    graduationdate = db.Column(db.DateTime)
    user_type = db.Column(db.String(20), default="Student")

    # Programming languages the student is proficient with
    languages = db.relationship(
        "ProgrammingLanguage",
        secondary=studentLanguages,
        primaryjoin=(studentLanguages.c.student_id == id),
        backref=db.backref("studentLanguages", lazy="dynamic"),
        lazy="dynamic",
    )

    # Topics of interest coincides with research Areas in faculty
    topics_of_interest = db.relationship(
        "ResearchField",
        secondary=studentFields,
        primaryjoin=(studentFields.c.student_id == id),
        backref=db.backref("studentFields", lazy="dynamic"),
        lazy="dynamic",
    )
    appliedPositions = db.relationship(
        "Applications", back_populates="student_enrolled"
    )

    def has_applied_to_position(self, position):
        return Applications.query.filter_by(studentID=self.id, position=position).first() is not None
        

    __mapper_args__ = {"polymorphic_identity": UserType.Student}

    def __repr__(self):
        """
        Converts the student object to a string
        Returns:
           String representation of the student object
        """
        return "<Student {} - {} - {}>".format(self.id, self.firstname, self.lastname)

    # By using set_password, we don't store the user's password, increasing security
    def set_password(self, password):
        """
        Sets the password of the student, hashing it for security
        Args:
            password: String, the password to be hashed
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# A sub-class of User, representing the faculty users
class Faculty(User):
    """
    Represents a faculty user, inheriting from User
    Attributes:
        __tablename__: String for inheritance
        id: Foreign key to User, primary key
        department: String, max 20 characters, department that faculty works in
        user_type: String, max 20 characters
        __mapper_args__: Polymorphic identity for inheritance
        password_hash: String, max 20 characters, password hash for security
    """

    __tablename__ = "faculty"
    # Research Areas coincide with Topics of Interest in the Student model
    id = db.Column(None, ForeignKey("user.id"), primary_key=True)
    researchAreas = db.Column(db.String(150))
    department = db.Column(db.String(20), db.ForeignKey("department.id"))
    user_type = db.Column(db.String(20), default="Faculty")

    research_areas = db.relationship(
        "ResearchField",
        secondary=facultyInterests,
        primaryjoin=(facultyInterests.c.faculty_id == id),
        backref=(db.backref("facultyInterests", lazy="dynamic")),
        lazy="dynamic",
    )

    __mapper_args__ = {"polymorphic_identity": UserType.Faculty}

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
class ResearchField(db.Model):
    """
    Represents the research fields that one may be interested in, and that some positions may pertain to
    Attributes:
        id: Integer, primary key
        title: String, max 30 characters
        attachedPosition: Many-to-many relationship with PositionField
        student_interested: Many-to-many relationship with Student
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    attachedPosition = db.relationship("PositionField", back_populates="fields")

    student_interested = db.relationship(
        "Student",
        secondary=studentFields,
        primaryjoin=(studentFields.c.field_id == id),
        backref=db.backref("studentFields", lazy="dynamic"),
        lazy="dynamic",
    )

    def get_fields(self):
        return self.query.all()

    def __repr__(self):
        return self.title


class ProgrammingLanguage(db.Model):
    """
    Represents the research fields that one may be interested in and that some positions may pertain to
    Attributes:
        id: Integer, primary key
        title: String, max 30 characters
        student_proficient: Many-to-many relationship with student
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))

    student_proficient = db.relationship(
        "Student",
        secondary=studentLanguages,
        primaryjoin=(studentLanguages.c.language_id == id),
        backref=db.backref("studentLanguages", lazy="dynamic"),
        lazy="dynamic",
    )

    position_required_by = db.relationship(
        "ResearchPosition",
        secondary=positionLanguages,
        primaryjoin=(positionLanguages.c.language_id == id),
        backref=db.backref("positionLanguages", lazy="dynamic"),
        lazy="dynamic",
    )

    def get_languages(self):
        return self.query.all()

    def __repr__(self):
        return self.title


# Represents the posted research positions
class ResearchPosition(db.Model):
    """
    Represents the research positions that are available for students to apply to
    Attributes:
        id: Integer, primary key
        title: String, max 30 characters
        wantedGPA: Float, the minimum GPA desired for the position
        languages: String, max 150 characters, the programming languages desired for the position
        description: String, max 1500 characters, the description of the position
        researchGoals: String, max 1500 characters, the goals of the research
        startDate: DateTime, the start date of the position
        endDate: DateTime, the end date of the position
        faculty: Integer, foreign key to Faculty
        students_application: One-to-many relationship with Applications
        researchFields: Many-to-many relationship with PositionField
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # Specifies the lowest desired GPA
    wantedGPA = db.Column(db.Float)
    languages = db.Column(db.String(150))
    description = db.Column(db.String(1500))
    researchGoals = db.Column(db.String(1500))
    startDate = db.Column(db.DateTime)
    endDate = db.Column(db.DateTime)
    timeCommitment = db.Column(db.Integer)
    faculty = db.Column(db.Integer, db.ForeignKey("faculty.id"))
    recommended = db.Column(db.Boolean, default=False)

    # Programming languages the position recommends
    languages = db.relationship(
        "ProgrammingLanguage",
        secondary=positionLanguages,
        primaryjoin=(positionLanguages.c.position_id == id),
        backref=db.backref("positionLanguages", lazy="dynamic"),
        lazy="dynamic",
    )

    students_application = db.relationship(
        "Applications", back_populates="enrolled_position"
    )
    researchFields = db.relationship("PositionField", back_populates="position")

    def topic_scorer(self, topics_of_interest) -> int:
        score = 0
        for topic in topics_of_interest:
            if self.researchGoals[1:-1].find(str(topic)) is not -1:
                score += 1
        return score

    def language_scorer(self, student_languages) -> int:
        score = 0
        for language in student_languages:
            if language in self.languages:
                score += 1
        return score

    def __repr__(self):
        return "<Research Position: {} -- Description: {}>".format(
            self.title, self.description
        )


# A relationship table relation research positions and the fields they pertain to
class PositionField(db.Model):
    """
    Represents the relationship between research positions and the fields they pertain to
    Attributes:
        pos_ID: Integer, foreign key to ResearchPosition
        field_ID: Integer, foreign key to ResearchField
        position: Relationship to ResearchPosition
        fields: Relationship to ResearchField
    """

    pos_ID = db.Column(
        db.Integer, db.ForeignKey("research_position.id"), primary_key=True
    )
    field_ID = db.Column(
        db.Integer, db.ForeignKey("research_field.id"), primary_key=True
    )

    # Represent relationships to Positions and ResearchFields respectively
    position = db.relationship("ResearchPosition")
    fields = db.relationship("ResearchField")


# A relationship table relating students to positions they have applied to
class Applications(db.Model):
    """
    Represents the applications that students have submitted to positions
    Attributes:
        studentID: Integer, foreign key to Student, primary key
        position: Integer, foreign key to ResearchPosition, primary key
        student_enrolled: Relationship to Student
        enrolled_position: Relationship to ResearchPosition
        statement_of_interest: String, max 1200 characters, the student's statement of interest
        referenceEmail: String, max 20 characters, the email of the reference
        referenceName: String, max 20 characters, the name of the reference
    """

    studentID = db.Column(db.Integer, db.ForeignKey("student.id"), primary_key=True)
    position = db.Column(
        db.Integer, db.ForeignKey("research_position.id"), primary_key=True
    )

    # Represent relationships to student and ResearchPosition respectively
    student_enrolled = db.relationship("Student")
    enrolled_position = db.relationship("ResearchPosition")

    # status
    status = db.Column(db.String(10), default="Pending")

    # applied date
    applied_date = db.Column(db.DateTime, default=datetime.now())

    # statement of interest
    statement_of_interest = db.Column(db.String(1500))

    # reference Info
    referenceEmail = db.Column(db.String(20))
    referenceName = db.Column(db.String(20))

    def __repr__(self):
        return "<studentID: {} --- position: {}>".format(self.studentID, self.position)


class Major(db.Model):
    """
    A Student's major
    Attributes:
        id: Integer, primary key
        name: String, unique
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    department = db.Column(db.Integer, db.ForeignKey("department.id"))


@login.user_loader
def load_user(id):
    student = Student.query.filter_by(id=id).first()
    if student:
        return student

    faculty = Faculty.query.filter_by(id=id).first()
    if faculty:
        return faculty

    return None
