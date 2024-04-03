from flask import Blueprint
from flask import render_template
from config import Config

routes_blueprint = Blueprint('routes', __name__)
routes_blueprint.template_folder = Config.TEMPLATE_FOLDER

@routes_blueprint.route('/', methods=['GET', 'POST'])
@routes_blueprint.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Index')