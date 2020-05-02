from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, SignupForm
from .. import db
from ..models import User

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(name=form.username.data,
                password=form.password.data)

        # add to database
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered!')

        # exit gracefully
        return redirect(url_for('auth.login'))

    # load the registration page
    return render_template('auth/register.html', form=form, title='Registration')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()

        # if we can validate, redirect to that dashboard
        if user is not None and user.verify_password(form.password.data):
            # log them in
            login_user(user)
            # redirect to dash
            return redirect(url_for('home.dashboard'))
        else:
            flash('Invalid username or password.')        

    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out.')
    return redirect(url_for('auth.login'))