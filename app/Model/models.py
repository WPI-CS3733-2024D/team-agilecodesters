from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return Student.query.get(int(id))

#A class representing a student user
class Student(db.Model):
    #Students are identified by their wpi_id
    wpi_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    #A hash of the password, kept as a hash for security
    password_hash = db.Column(db.String(20))
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    email = db.Column(db.String(20))
    phone = db.Column(db.String(10))
    major = db.Column(db.String(20))
    GPA = db.Column(db.Float)
    graduationdate = db.Column(db.String(20))
    #Topics of interest coincides with research Areas in faculty
    topics_of_interest = db.Column(db.String)

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
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(20))
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    email = db.Column(db.String(20))
    phone = db.Column(db.String(10))
    #Research Areas coincide with Topics of Interest in the Student model
    researchAreas = db.Column(db.String)

    def __repr__(self):
         return '<Faculty {} - {} - {}>'.format(self.wpi_id, self.firstname, self.lastname)
        
    #By using set_password, we don't store the user's password, increasing security
    def set_password(self, password):
            self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)