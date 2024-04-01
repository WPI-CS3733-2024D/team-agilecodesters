from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Student(db.Model):
    wpi_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(20))
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    email = db.Column(db.String(20))
    phone = db.Column(db.String(10))
    major = db.Column(db.String(20))
    GPA = db.Column(db.Double)
    graduationdate = db.Column(db.String(20))
    Topics_of_interest = db.Column(db.String)
