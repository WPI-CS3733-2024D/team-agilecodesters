from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import  ValidationError, Length, DataRequired, Email, EqualTo
from app.Model.models import Student

class StudentRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    #email = StringField('Email', validators=[DataRequired(), Email()])
    #firstname = StringField('First Name', validators=[DataRequired()])
    #lastname = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    #major = StringField('Major', validators=[DataRequired()])
    #gpa = FloatField('GPA', validators=[DataRequired()])
    #graduation_date = StringField('Graduation Date', validators=[DataRequired()])
    #topics_of_interest = TextAreaField('Topics of Interest', validators=[Length(max=200)])
    submit = SubmitField('Register')

class FacultyRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    research_areas = TextAreaField('Research Areas', validators=[Length(max=200)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')