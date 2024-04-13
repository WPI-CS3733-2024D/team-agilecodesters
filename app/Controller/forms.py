from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms import DateField, SelectField, SelectMultipleField, StringField, SubmitField, TextAreaField, PasswordField, FloatField, DateTimeField, validators
from wtforms.validators import  ValidationError, Length, DataRequired, Email, EqualTo
from app.Model.models import ResearchField, Student
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.widgets import ListWidget, CheckboxInput
from flask_login import current_user

def validate_phone_number(form, field):
    if not field.data.isdigit():
        raise validators.ValidationError('Phone number must contain only numbers!')
    if not len(field.data) == 10:
        raise validators.ValidationError('Phone number must be 10 digits long!')

class ApplicationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    statement_of_interest = TextAreaField("Body",  validators=[DataRequired(), Length(max=1500)])
    reference_faculty_firstname = StringField('Reference First Name', validators=[DataRequired()])
    reference_faculty_lastname = StringField('Reference Last Name', validators=[DataRequired()])
    reference_faculty_email = StringField('Reference Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

    # TODO Jonathan(self): Write code logic for getting a professor to send a letter of recommendation

class PostPositionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    wantedGPA = FloatField('Lowest Desired GPA', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired(), Length(max=1500)])
    researchGoals = StringField('Research Goals', validators=[DataRequired()])
    startDate = DateField('Start Date', validators=[DataRequired()])
    endDate = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('Post')

# SEARCH FEATURE on index page
class SearchForm(FlaskForm):
    sortOrder = SelectField('Sort by:', choices=[('Date', 'Start Date'), ('GPA', 'Highest Required GPA'), ('Fields', 'Research Fields')], default='Date')
    submit = SubmitField('Search')
    def get_choices(self):
        return self.sortOrder.choices
    
class EditStudentProfileForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    phone_number = StringField("Phone Number", validators=[DataRequired(), validate_phone_number])
    email = StringField('Email', validators=[DataRequired(), Email()])
    major = StringField('Major', validators=[DataRequired()])
    GPA = FloatField('GPA', validators=[DataRequired()])
    graduationdate = DateField('Graduation Date', validators=[DataRequired()])
    topics_of_interest = QuerySelectMultipleField(
        "Topics of Interest",
        query_factory=lambda: ResearchField.query.all(),
        get_label=lambda x: x.title,
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput(),
    )
    other_topics = StringField("Topics Not Listed Above, Please Separate with Commas")
    password = PasswordField('Password', validators=[DataRequired()])
    password_2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Save Changes')

class EditFacultyProfileForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    phone_number = StringField("Phone Number", validators=[DataRequired(), validate_phone_number])
    email = StringField('Email', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    research_areas = QuerySelectMultipleField(
        "Research Areas",
        query_factory=lambda: ResearchField.query.all(),
        get_label=lambda x: x.title,
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput(),
    )
    other_areas = StringField("Research Areas Not Listed Above, Please Separate with Commas")
    password = PasswordField('Password', validators=[DataRequired()])
    password_2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Save Changes')