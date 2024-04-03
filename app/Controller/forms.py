from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, IntegerField, FloatField, SelectField
from wtforms.validators import  ValidationError, Length, DataRequired, Email, EqualTo, NumberRange 
from app.Model.models import Student, Faculty
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_login import current_user

class EditRegFormStudent(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    gpa = FloatField("Enter GPA", validators=[DataRequired(), NumberRange(min=0.0, max=4.0)])
    wpi_id = IntegerField("Identification Number", validators=[DataRequired(), NumberRange(min=6, max=9)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Address', [Length(min=0, max=200)]) # TextAreaField makes an adjustedable textbox
    password = PasswordField('Password', validators=[DataRequired()])
    topics_of_interest = TextAreaField('Topics of Interest')
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')]) # make sure passwords are the same
    submit = SubmitField('Submit')

    def validate_email(self, email):
        students = Student.query.filter_by(email = email.data).all()

        for student in students: 
            if (student.id != current_user.id):
                raise ValidationError('The email is associated with another account! Use a different email address')
            
class EditRegFormFaculty(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    wpi_id = IntegerField("Identification Number", validators=[DataRequired(), NumberRange(min=6, max=9)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Address', [Length(min=0, max=200)]) # TextAreaField makes an adjustedable textbox
    password = PasswordField('Password', validators=[DataRequired()])
    topics_of_interest = TextAreaField('Topics of Interest')
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')]) # make sure passwords are the same
    submit = SubmitField('Submit')

    def validate_email(self, email):
        faculty_emails = Faculty.query.filter_by(email = email.data).all()

        for faculty in faculty_emails: 
            if (faculty.wpi_id != current_user.wpi_id):
                raise ValidationError('The email is associated with another account! Use a different email address')
            
class createPosForm():
    title = StringField('Enter Title of Research Position',  validators=[DataRequired()])
    Description = StringField('Enter the description')
    start_date = StringField('Start Date', validators=[DataRequired()])
    end_date = StringField('End Date', validators=[DataRequired()])
    description = StringField('Enter Description', validators=[DataRequired()])
    time_commitment = StringField('Enter Time Commitment', validators=[DataRequired()])
    research_fields = SelectField('Choose an Option', 
        validators=[DataRequired()],  choices=[('machinelearning', 'Machine Learning and Artificial Intelligence'), 
                                               ('climatescience', 'Climate Science'), 
                                               ('quantumcomputing', 'Quantum Computing'), 
                                               ('biotechnology', 'Biotechnology'), 
                                               ('neuroscience', 'Neuroscience'), 
                                               ('materialscience', 'Material Science')])
        
class applicationForm():
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    statement_of_interest = TextAreaField("Body",  validators=[DataRequired(), Length(max=1500)])
    reference_faculty_firstname = StringField('Reference First Name', validators=[DataRequired()])
    reference_faculty_lasntame = StringField('Reference Last Name', validators=[DataRequired()])
    reference_faculty_email = StringField('Reference Email', validators=[DataRequired()])

    # TODO Jonathan(self): possibly write code to check if the email is valid.
    # TODO Jonathan(self): Write code logic for getting a professor to send a letter of recommendation
    