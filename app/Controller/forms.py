from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms import DateField, SelectField, SelectMultipleField, StringField, SubmitField, TextAreaField, PasswordField, FloatField, DateTimeField
from wtforms.validators import  ValidationError, Length, DataRequired, Email, EqualTo
from app.Model.models import ResearchField, Student
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.widgets import ListWidget, CheckboxInput
from flask_login import current_user


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
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
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
    submit = SubmitField('Save Changes')

class EditFacultyProfileForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    phone = StringField('Phone')
    department = StringField('Department', validators=[DataRequired()])
    submit = SubmitField('Save Changes')