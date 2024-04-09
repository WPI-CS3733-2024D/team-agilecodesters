from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.Controller.forms import postPositionForm, searchForm
from app.Model.models import Applications, ResearchPosition
from config import Config
from app import db

routes_blueprint = Blueprint('routes', __name__)
routes_blueprint.template_folder = Config.TEMPLATE_FOLDER

@routes_blueprint.route('/', methods=['GET', 'POST'])
@routes_blueprint.route('/index/student', methods=['GET', 'POST'])
@login_required
def index_student():
    # add logic to filter out research positions based on searches.
    # research positions that align with student queried information [search feature] will show on the screen.
    search_form = searchForm()
    posts = ResearchPosition.query.all()
    return render_template('index_student.html', title='Student Home', posts=posts, search_form = search_form)

@routes_blueprint.route('/index/faculty', methods=['GET', 'POST'])
@login_required
def index_faculty():
    return render_template('index_faculty.html', title='Faculty Home')

@routes_blueprint.route('/create_position', methods=['GET', 'POST'])
@login_required
def create_position():
    form = postPositionForm()
    if form.validate_on_submit():
        position = ResearchPosition(title=form.title.data, wantedGPA=form.wantedGPA.data, description=form.description.data, researchGoals=form.researchGoals.data, startDate=form.startDate.data, endDate=form.endDate.data)
        #TODO: Add faculty information, not sure what current_user is capable of? Could be because db hasn't been restarted
        #position.faculty_email = current_user.data.
        db.session.add(position)
        db.session.commit()
        return redirect(url_for('routes.index'))
    return render_template('_create-position.html', title='Create Position')

@routes_blueprint.route('/apply/<position_id>', methods=['POST'])
@login_required
def apply_for_position(position_id):
    wpi_id = current_user.wpi_id
    application = Applications(studentID=wpi_id, position=position_id)
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

@routes_blueprint.route('/post/<position_id>', methods=['GET', 'POST'])
@login_required
def view_post(position_id):
    return render_template('view_post.html', title='Profile', position_id=position_id)

@routes_blueprint.route('/profile', methods=['GET'])
@login_required
def view_profile():
    return render_template('profile.html', title='Profile')

@routes_blueprint.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    return render_template('edit_profile.html', title='Edit Profile')