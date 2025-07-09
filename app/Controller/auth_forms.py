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
from app.Model.models import Department, Major, ProgrammingLanguage, ResearchField
from wtforms.widgets import ListWidget, CheckboxInput

# This file contains the forms used for user registration and login in the application for students and professors.

# CONCEPT: Forms is used to collect data from users in a structured way. This data will then by 
#   processed by the server and stored in the database.

# helps with validating phone numbers and checking the appropiate length and data inputted in this section
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


    major = QuerySelectField( # dropdown menu for majors.
        
        # get all major objects from database
        # Displays each major's name using the name attribute from teh major table model.
        "Major", query_factory=lambda: Major.query.all(), get_label=lambda x: x.name 
    )

    # decimal for required GPA data input.
    gpa = FloatField("GPA", validators=[DataRequired()])
    graduation_date = DateField("Graduation Date", validators=[DataRequired()])

    # dropdown menu for topics of interest.
    # gets all the research fields stored in the database.
    # goes through every research field and gets the title attribute to display.
    # makes it a checkbox input.
    topics_of_interest = QuerySelectMultipleField(
        "Topics of Interest",
        query_factory=lambda: ResearchField.query.all(),
        get_label=lambda x: x.title,
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput(),
    )

    # another text box field for entering topics not mentioned in dropdown menu.
    other_topics = StringField("Topics Not Listed Above, Please Separate with Commas")

    # looks at programming languages table in the database.
    # gets all programming language objects from the database.
    # displays specificially their title attribute.
    # this is a chechbox input to select multiple languages.
    languages = QuerySelectMultipleField(
        "Programming Languages",
        query_factory=lambda: ProgrammingLanguage.query.all(),
        get_label=lambda x: x.title,
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput(),
    )

    # any other languages are separated by commas in a text box.
    other_languages = StringField(
        "Languages Not Listed Above, Please Separate with Commas"
    )

    # ensure both passwords fields are typed and match to ensure security.
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )

    # submit button for the form. when clicked, registration form data is submitted to the server.
    submit = SubmitField("Register")


class FacultyRegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()]) 

    # uses helper function to check validaty of phone number.
    phone_number = StringField(
        "Phone Number", validators=[DataRequired(), validate_phone_number]
    )

    # gets all department objects from database and lists the names.
    # displays their name attribute of every department in the dropdown menu.
    department = QuerySelectField(
        "Department",
        query_factory=lambda: Department.query.all(),
        get_label=lambda x: x.name,
    )

    # gets all research fields from the database.
    # gets all research field objects from the database.
    # gets all research field titles to display in the dropdown menu.
    # this is a chechbox input allowing you to select multiple research areas.
    research_areas = QuerySelectMultipleField(
        "Research Areas",
        query_factory=lambda: ResearchField.query.all(),
        get_label=lambda x: x.title,
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput(),
    )

    # text box for entering any other research areas not listed in the dropdown menu.
    other_topics = StringField(
        "Research Areas Not Listed Above, Please Separate with Commas"
    )
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):

    # Form for logging in users.
    # Contains fields for username, password, and remember me option.
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign in")
