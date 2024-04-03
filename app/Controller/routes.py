from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.Controller.forms import postPositionForm
from app.Model.models import ResearchPosition
from config import Config
from app import db

routes_blueprint = Blueprint('routes', __name__)
routes_blueprint.template_folder = Config.TEMPLATE_FOLDER

@routes_blueprint.route('/', methods=['GET', 'POST'])
@routes_blueprint.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Index')


@routes_blueprint.route('/create_position', methods=['GET', 'POST'])
def create_post():
    form = postPositionForm()
    if form.validate_on_submit():
        position = ResearchPosition(title=form.title.data,wantedGPA=form.wantedGPA.data, description=form.description.data, researchGoals=form.researchGoals.data, startDate=form.startDate.data, endDate=form.endDate.data)
        #TODO: Add faculty information, not sure what current_user is capable of? Could be because db hasn't been restarted
        #position.faculty_email = current_user.data.
        db.session.add(position)
        db.session.commit()
        return redirect(url_for('routes.index'))
    return render_template('_create-position.html', title='Create Position')