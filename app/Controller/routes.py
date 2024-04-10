from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from app.Controller.forms import ApplicationForm, EditFacultyProfileForm, EditStudentProfileForm, PostPositionForm, SearchForm
from app.Model.models import Applications, PositionField, ResearchField, ResearchPosition
from config import Config
from app import db

routes_blueprint = Blueprint('routes', __name__)
routes_blueprint.template_folder = Config.TEMPLATE_FOLDER

@routes_blueprint.route('/', methods=['GET', 'POST'])
@routes_blueprint.route('/index', methods=['GET', 'POST'])
@routes_blueprint.route('/index/student', methods=['GET', 'POST'])
@login_required
def index_student():
    if (current_user.user_type != 'Student'):
        return redirect(url_for('routes.index_faculty'))
    # add logic to filter out research positions based on searches.
    # research positions that align with student queried information [search feature] will show on the screen.
    search_form = SearchForm()
    posts = ResearchPosition.query.order_by(ResearchPosition.startDate.desc())
    if search_form.validate_on_submit():
        if search_form.get_choices()[2] == search_form.sortOrder.data: #Research Fields
            # Query the ResearchPosition objects that share at least one field with the student
            shared_positions = ResearchPosition.query.join(PositionField).join(ResearchField).filter(PositionField.field_ID.in_([field.id for field in current_user.topics_of_interest])).all()
            posts = shared_positions
        elif search_form.get_choices()[1] == search_form.sortOrder.data: #Highest Required GPA
            posts = ResearchPosition.query.order_by(ResearchPosition.wantedGPA.desc())
        else: #Start date by default
            posts = ResearchPosition.query.order_by(ResearchPosition.startDate.desc())
    return render_template('index_student.html', title='Student Home', posts=posts.all(), search_form = search_form)

@routes_blueprint.route('/index/faculty', methods=['GET', 'POST'])
@login_required
def index_faculty():
    if (current_user.user_type != 'Faculty'):
        return redirect(url_for('routes.index_student'))
    return render_template('index_faculty.html', title='Faculty Home')

@routes_blueprint.route('/create_position', methods=['GET', 'POST'])
@login_required
def create_position():
    form = PostPositionForm()
    if form.validate_on_submit():
        position = ResearchPosition(title=form.title.data, wantedGPA=form.wantedGPA.data, description=form.description.data, researchGoals=form.researchGoals.data, startDate=form.startDate.data, endDate=form.endDate.data)
        position.faculty = current_user
        db.session.add(position)
        db.session.commit()
        return redirect(url_for('routes.index_student'))
    return render_template('_create-position.html', title='Create Position')

@routes_blueprint.route('/apply/<position_id>', methods=['POST'])
@login_required
def apply_for_position(position_id):
    position = ResearchPosition.query.get(position_id)
    aform = ApplicationForm()
    if aform.validate_on_submit():
        application = Applications(studentID=current_user.id, position=position_id,statement_of_interest=aform.statement_of_interest.data, 
                                   referenceName=aform.reference_faculty_firstname + " " + aform.reference_faculty_lastname, 
                                   referenceEmail = aform.reference_faculty_email)

        db.session.add(application)
        db.session.commit()
        flash('Application submitted successfully!')
        return redirect(url_for('routes.index_student'))
    else:
        aform.firstname.data = current_user.firstname
        aform.lastname.data = current_user.lastname
    return render_template('_apply.html', form = aform, position_id = position_id, position_title=position.title)

@routes_blueprint.route('/unapply/<position_id>', methods=['POST'])
@login_required
def unapply_for_position(position_id):
    application = Applications.query.filter_by(studentID=current_user.wpi_id, position=position_id).first()
    if application:
        db.session.delete(application)
        db.session.commit()
        flash('Successfully unapplied for the position.')
    return redirect(url_for('routes.index_student'))

@routes_blueprint.route('/position/<position_id>', methods=['GET', 'POST'])
@login_required
def view_position(position_id):
    position = ResearchPosition.query.get(position_id)
    return render_template('view_position.html', title='Profile', position=position)

@routes_blueprint.route('/profile', methods=['GET'])
@login_required
def view_profile():
    return render_template('profile.html', title='Profile')

@routes_blueprint.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if current_user.user_type == 'Student':
        form = EditStudentProfileForm()
    else:
        form = EditFacultyProfileForm()
    if request.method == 'POST':
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data
        current_user.set_password(form.password.data)
        current_user.major = form.major.data
        current_user.GPA = form.GPA.data
        current_user.graduationdate = form.graduationdate.data
        #current_user.topics_of_interest = form.topics_of_interest.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your profile has been updated!')
        return redirect(url_for('routes.view_profile'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.email.data = current_user.email
        form.major.data = current_user.major
        form.GPA.data = current_user.GPA
        #form.graduationdate.data = current_user.graduationdate
        #form.topics_of_interest.data = [topic.id for topic in current_user.topics_of_interest]
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@routes_blueprint.route('/profile/positions', methods=['GET', 'POST'])
@login_required
def view_applied():
    if current_user.user_type == 'Student':
        applications = Applications.query.filter_by(studentID=current_user.id).all()
    return render_template('view_applied.html', title='Applied Positions', applications=applications)