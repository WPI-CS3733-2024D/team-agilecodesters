from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, FloatField, DateTimeField
from wtforms.validators import  ValidationError, Length, DataRequired, Email, EqualTo
from app.Model.models import Student
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_login import current_user


class applicationForm():
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    statement_of_interest = TextAreaField("Body",  validators=[DataRequired(), Length(max=1500)])
    reference_faculty_firstname = StringField('Reference First Name', validators=[DataRequired()])
    reference_faculty_lasntame = StringField('Reference Last Name', validators=[DataRequired()])
    reference_faculty_email = StringField('Reference Email', validators=[DataRequired()])

    # TODO Jonathan(self): possibly write code to check if the email is valid.
    # TODO Jonathan(self): Write code logic for getting a professor to send a letter of recommendation

class postPositionForm():
    title = StringField('Title', validators=[DataRequired()])
    wantedGPA = FloatField('Lowest Desired GPA', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired(), Length(max=1500)])
    researchGoals = StringField('Research Goals', validators=[DataRequired()])
    startDate = DateTimeField('Start Date', validators=[DataRequired()])
    endDate = DateTimeField('End Date', validators=[DataRequired()])