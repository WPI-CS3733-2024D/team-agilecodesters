from flask import render_template, Blueprint
from config import Config

auth_blueprint = Blueprint('auth', __name__)
auth_blueprint.template_folder = Config.TEMPLATE_FOLDER

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title='Login')

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', title='Register')