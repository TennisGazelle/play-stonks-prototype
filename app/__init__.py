from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# local imports
from config import app_config


# after existing third-party imports
from flask_login import LoginManager

# after the db variable initialization
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # add
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)  # add
    db.init_app(app)

    # login_manager.init_app(app)
    # login_manager.login_message = "You must be logged in to access this page."
    # login_manager.login_view = "auth.login"

    # migrate = Migrate(app, db)

    # from app import models

    @app.route('/')
    def hello_world():
        return render_template('index.html')

    return app