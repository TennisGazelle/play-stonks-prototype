from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

# local imports
from config import app_config

# after the db variable initialization
login_manager = LoginManager()
db = SQLAlchemy()  # add


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')
    # app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # add
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    migrate = Migrate(app, db)

    Bootstrap(app)

    from app import models

    from .admin import admin as admin_blueprint
    from .auth import auth as auth_blueprint
    from .home import home as home_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(home_blueprint)

    # @app.route('/')
    # def hello_world():
    #     return render_template('index.html')

    return app