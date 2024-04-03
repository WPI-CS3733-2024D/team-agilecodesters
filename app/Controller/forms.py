from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import  ValidationError, Length, DataRequired, Email, EqualTo
from app.Model.models import Student
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_login import current_user

class EditRegForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
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