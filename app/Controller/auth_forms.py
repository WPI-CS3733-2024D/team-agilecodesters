from flask_wtf import FlaskForm
from wtforms import (
    FloatField,
    StringField,
    SubmitField,
    TextAreaField,
    PasswordField,
    BooleanField,
)
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import ValidationError, Length, DataRequired, Email, EqualTo
from app.Model.models import Student, ResearchField
from wtforms.widgets import ListWidget, CheckboxInput


class StudentRegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    major = StringField("Major", validators=[DataRequired()])
    gpa = FloatField("GPA", validators=[DataRequired()])
    graduation_date = StringField("Graduation Date", validators=[DataRequired()])
    topics_of_interest = QuerySelectMultipleField(
        "Topics of Interest",
        query_factory=lambda: ResearchField.query.all(),
        get_label=lambda x: x.title,
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput(),
    )
    other_topics = StringField("Topics Not Listed Above, Please Separate with Commas")
    submit = SubmitField("Register")


class FacultyRegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    research_areas = QuerySelectMultipleField(
        "Research Areas",
        query_factory=lambda: ResearchField.query.all(),
        get_label=lambda x: x.title,
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput(),
    )
    other_topics = StringField("Topics Not Listed Above, Please Separate with Commas")
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign in")
