from flask import render_template, request
from flask_login import login_required

from . import home
from ..models import User

@home.route('/')
def homepage():
    return render_template('index.html', title='Welcome')

@home.route('/dashboard')
def dashboard():
    this_user_name = User.query.order_by(User.id).first().name
    return render_template('home/dashboard.html', title='Dashboard', name=this_user_name)

