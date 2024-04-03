from flask import flash, redirect, render_template, Blueprint, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app.Controller.auth_forms import LoginForm
from app.Model.models import Student
from config import Config
from app import db

auth_blueprint = Blueprint('auth', __name__)
auth_blueprint.template_folder = Config.TEMPLATE_FOLDER

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', title = "Register")

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    lform = LoginForm()
    if lform.validate_on_submit():
        student = Student.query.filter_by(username = lform.username.data).first()
        #if login fails
        if (student is None) or (student.check_password(lform.password.data) == False):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(student, remember = lform.remember_me.data)
        return redirect(url_for('routes.index'))
    return render_template('login.html', title='Sign in', form = lform)

@auth_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))