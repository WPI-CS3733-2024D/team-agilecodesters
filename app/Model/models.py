from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(wpi_id):
    return Student.query.get(int(wpi_id))

#A class representing a student user
class Student(db.Model):
    #Students are identified by their wpi_id
    wpi_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    #A hash of the password, kept as a hash for security
    password_hash = db.Column(db.String(20))
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    email = db.Column(db.String(20), unique=True)
    phone = db.Column(db.String(10))
    major = db.Column(db.String(20))
    GPA = db.Column(db.Float)
    graduationdate = db.Column(db.String(20))
    #Topics of interest coincides with research Areas in faculty
    topics_of_interest = db.Column(db.String)
    statement_of_interest = db.Column(db.String)

    appliedPositions = db.relationship('EnrolledPositions', back_populates='student_enrolled')

    def __repr__(self):
        return '<Student {} - {} - {}>'.format(self.wpi_id, self.firstname, self.lastname)
    
    #By using set_password, we don't store the user's password, increasing security
    def set_password(self, password):
            self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

#A class representing the faculty users
class Faculty(db.Model):
    #Faculty are identified by their wpi_id
    wpi_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(20))
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    email = db.Column(db.String(20), unique=True)
    phone = db.Column(db.String(10))
    #Research Areas coincide with Topics of Interest in the Student model
    researchAreas = db.Column(db.String(150))

    def __repr__(self):
         return '<Faculty {} - {} - {}>'.format(self.wpi_id, self.firstname, self.lastname)
        
    #By using set_password, we don't store the user's password, increasing security
    def set_password(self, password):
            self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
#Represents the posted research positions
class ResearchPosition(db.Model):
    #The primary key is a unique title given by the poster
    title = db.Column(db.String(30), unique=True, primary_key=True)
    topics = db.Column(db.String(150))
    #Specifies the lowest desired GPA
    wantedGPA = db.Column(db.Float)
    languages = db.Column(db.String(150))
    description = db.Column(db.String(1500))
    researchGoals = db.Column(db.String(1500))
    startDate = db.Column(db.DateTime)
    endDate = db.Column(db.DateTime)
    faculty_name = db.Column(db.String(20))
    faculty_email = db.Column(db.String(20), db.ForeignKey('faculty.email'))

    students_application = db.relationship('Student_App', back_populates='enrolled_position')

    def __repr__(self):
         return '<Research Position: {} -- Description: {}>'.format(self.title, self.description)

#A relationship table relating students to positions they have applied to
class EnrolledPosition(db.Model):
    studentID = db.Column(db.Integer, db.ForeignKey('student.wpi_id'), primary_key=True)
    position = db.Column(db.String(20), db.ForeignKey('researchposition.title'), primary_key=True)

    #Represent relationships to student and ResearchPosition respectively
    student_erolled = db.relationship('Student')
    enrolled_position = db.relationship('ResearchPosition')

    def __repr__(self):
          return '<studentID: {} --- position: {}>'.format(self.studentID, self.position)