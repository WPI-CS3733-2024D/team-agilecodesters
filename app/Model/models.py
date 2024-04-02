from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return Student.query.get(int(id))

class Student(db.Model):
    wpi_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(20))
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    email = db.Column(db.String(20))
    phone = db.Column(db.String(10))
    major = db.Column(db.String(20))
    GPA = db.Column(db.Float)
    graduationdate = db.Column(db.String(20))
    topics_of_interest = db.Column(db.String)

    def __repr__(self):
        return '<Student {} - {} - {}>'.format(self.id, self.firstname, self.lastname, self.email)
    
    def set_password(self, password):
            self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
