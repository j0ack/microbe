#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Users models for Microbe app
"""

from werkzeug.security import check_password_hash, generate_password_hash

from microbe.database import db

__author__ = u'TROUVERIE Joachim'


class User(db.Model):
    """User class
    :param name: user name
    :param password: user password
    :param email: user email
    :param hashed: if the given password is hashed
    :type name: str
    :type password: str
    :type email: str
    :type hashed: bool
    """
    __tablename__ = 'User'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(40))
    password = db.Column(db.String(80))

    def __init__(self, name, password, email, hashed=False):
        self.name = name
        self.email = email
        # hash password if necessary
        if not hashed:
            self.set_password(password)
        else:
            self.password = password

    def __repr__(self):
        return '<User {0}>'.format(self.name)

    def set_password(self, clear_password):
        """Registered hashed password"""
        self.password = generate_password_hash(clear_password)

    def check_password(self, password):
        """Check password hash
        :param password: unhashed password to check
        :type password: str
        """
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
