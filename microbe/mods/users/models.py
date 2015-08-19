#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Users models for Microbe app
"""

import shelve
from werkzeug.security import check_password_hash, generate_password_hash

from flask import current_app

__author__ = 'TROUVERIE Joachim'


class Users(object):
    """Users API class providing static methods to work with users"""
    @staticmethod
    def get(username):
        """Get user by username"""
        # get password hash for username
        dic = current_app.config['USERS']
        dic = dic.get(username)
        if not dic:
            return None
        # create object
        return User(dic.get('name'), dic.get('pw_hash'),
                    dic.get('email'), True)

    @staticmethod
    def delete(username):
        """Delete user by username"""
        # get config
        path = current_app.config['SHELVE_FILENAME']
        db = shelve.open(path)
        dic = db['USERS']
        # delete entry
        del dic[username]
        # update config
        db['USERS'] = dic
        db.close()

    @staticmethod
    def update(username, email, password):
        """Add or update a user"""
        # get config
        path = current_app.config['SHELVE_FILENAME']
        db = shelve.open(path)
        dic = db.get('USERS', {})
        # create object
        user = User(username, password, email)
        # create new entry or update value
        dic[username] = user.__dict__
        # update config
        db['USERS'] = dic
        db.close()


class User(object):
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
    def __init__(self, name, password, email, hashed=False):
        self.name = name
        self.email = email
        # hash password if necessary
        if not hashed:
            self.pw_hash = generate_password_hash(password)
        else:
            self.pw_hash = password

    def check_password(self, password):
        """Check password hash

        :param password: unhashed password to check
        :type password: str
        """
        return check_password_hash(self.pw_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.name)
