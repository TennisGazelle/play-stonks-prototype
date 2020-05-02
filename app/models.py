import re
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

import pymysql
pymysql.install_as_MySQLdb()

from app import db, login_manager

class Sentence(db.Model):
    """
    Create an Sentence table
    """
    __tablename__ = 'sentences'

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), index=True)
    target = db.Column(db.String(100), index=True)
    template = db.Column(db.String(100), index=True) # must have two "{}" in it
    for_who = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        if re.search('.*{*}*{*}*.*', self.template):
            return '<Sentence: {}>'.format(self.template.format(self.action, self.target))
        else:
            return '<Sentence: {} {}>'.format(self.action, self.target)


class Objective(db.Model):
    """
    Create an Objective Table
    """
    __tablename__ = 'objectives'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    is_admin = db.Column(db.Boolean, default=False)
    sentence = db.Column(db.Integer, db.ForeignKey('sentences.id'))

    def __repr__(self):
        return '<Objective: {}>'.format(self.name)


class User(UserMixin, db.Model):
    """
    Create a User Table
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    address = db.Column(db.String(200), index=True)
    savings_to_checking_ratio = db.Column(db.Float, index=True)
    total_spending_money = db.Column(db.Integer, index=True)
    total_debt = db.Column(db.Integer, index=True)
    password_hash = db.Column(db.String(128))
    # array of objectives
    # objectives = db.relationship('Objective', backref='user', lazy='dynamic')
    # array of levels
    # array of abilities

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        if self.password_hash:
            print('user {} has no password hash!!')
            return True
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.name)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
