from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.Controller.forms import applicationForm, postPositionForm, searchForm
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
    if ('student' != 'student'):
        return redirect(url_for('routes.index_faculty'))
    # add logic to filter out research positions based on searches.
    # research positions that align with student queried information [search feature] will show on the screen.
    search_form = searchForm()
    if search_form.get_choices()[2] == search_form.sortOrder.data: #Research Fields
        # Query the ResearchPosition objects that share at least one field with the student
        shared_positions = ResearchPosition.query.join(PositionField).join(ResearchField).filter(PositionField.field_ID.in_([field.id for field in current_user.topics_of_interest])).all()
        posts = shared_positions
    elif search_form.get_choices()[1] == search_form.sortOrder.data: #Highest Required GPA
        posts = ResearchPosition.query.order_by(ResearchPosition.wantedGPA.desc())
    else: #Start date by default
        posts = ResearchPosition.query.order_by(ResearchPosition.startDate.desc())
    return render_template('index_student.html', title='Student Home', posts=posts, search_form = search_form)

@routes_blueprint.route('/index/faculty', methods=['GET', 'POST'])
@login_required
def index_faculty():
    if ('student' != 'faculty'):
        return redirect(url_for('routes.index_student'))
    return render_template('index_faculty.html', title='Faculty Home')

@routes_blueprint.route('/create_position', methods=['GET', 'POST'])
@login_required
def create_position():
    form = postPositionForm()
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
    form = applicationForm()
    if form.validate_on_submit():
        id = current_user.id
        application = Applications(studentID=id, position=position_id,statement_of_interest=form.statement_of_interest.data, referenceName=form.reference_faculty_firstname + " " + form.reference_faculty_lastname, referenceEmail = form.reference_faculty_email)
        db.session.add(application)
        db.session.commit()
    flash('Application submitted successfully!')
    return redirect(url_for('routes.index_student'))

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
    return render_template('view_position.html', title='Profile', position_id=position_id)

@routes_blueprint.route('/profile', methods=['GET'])
@login_required
def view_profile():
    return render_template('profile.html', title='Profile')

@routes_blueprint.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    return render_template('edit_profile.html', title='Edit Profile')
