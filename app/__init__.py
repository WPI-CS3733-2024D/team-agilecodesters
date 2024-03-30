from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from config import Config

db = SQLAlchemy()
Bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'auth.login' # application needs to know which view function is configured for the login
moment = Moment()
# package app

# configure application according to what is defined in config class

# from app.Controller import routes, errors
# from app.Model import models

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.static_folder = config_class.STATIC_FOLDER
    app.template_folder = config_class.TEMPLATE_FOLDER
    # creates the database for communication
    db.init_app(app)
    login.init_app(app)
    moment.init_app(app)
    Bootstrap.init_app(app)
    #blue print registration
    from app.Controller.errors import errors_blueprint as errors
    app.register_blueprint(errors)
    from app.Controller.auth_routes import auth_blueprint as auth
    app.register_blueprint(auth)
    from app.Controller.routes import routes_blueprint as routes
    app.register_blueprint(routes)

    return app