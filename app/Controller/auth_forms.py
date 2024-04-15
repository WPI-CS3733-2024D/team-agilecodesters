from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    FloatField,
    StringField,
    SubmitField,
    PasswordField,
    BooleanField,
    validators,
)
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo
from app.Model.models import Department, Major, ResearchField
from wtforms.widgets import ListWidget, CheckboxInput


def validate_phone_number(form, field):
    if not field.data.isdigit():
        raise validators.ValidationError("Phone number must contain only numbers!")
    if not len(field.data) == 10:
        raise validators.ValidationError("Phone number must be 10 digits long!")


class StudentRegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone_number = StringField(
        "Phone Number", validators=[DataRequired(), validate_phone_number]
    )
    major = QuerySelectField(
        "Major", query_factory=lambda: Major.query.all(), get_label=lambda x: x.name
    )
    gpa = FloatField("GPA", validators=[DataRequired()])
    graduation_date = DateField("Graduation Date", validators=[DataRequired()])
    topics_of_interest = QuerySelectMultipleField(
        "Topics of Interest",
        query_factory=lambda: ResearchField.query.all(),
        get_label=lambda x: x.title,
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput(),
    )
    other_topics = StringField("Topics Not Listed Above, Please Separate with Commas")
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")


class FacultyRegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone_number = StringField(
        "Phone Number", validators=[DataRequired(), validate_phone_number]
    )
    department = QuerySelectField(
        "Department",
        query_factory=lambda: Department.query.all(),
        get_label=lambda x: x.name,
    )
    research_areas = QuerySelectMultipleField(
        "Research Areas",
        query_factory=lambda: ResearchField.query.all(),
        get_label=lambda x: x.title,
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput(),
    )
    other_topics = StringField("Topics Not Listed Above, Please Separate with Commas")
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign in")
