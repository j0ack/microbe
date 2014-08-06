#! /usr/bin/env python
#-*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    Classes for Microbe app
"""

__author__ = 'TROUVERIE Joachim'

import os
import re
from os.path import join, splitext
from uuid import uuid4
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from yaml import safe_dump

from flask import url_for
from flask.ext import shelve
from flask.ext.login import current_user


class Users(object) :
    """
        Users API class providing static methods to work with users
    """
    @staticmethod
    def get(username) :
        """
            Get user by username
        """
        # get password hash for username
        db = shelve.get_shelve('r')
        dic = db['USERS']
        pwd_hash = dic.get(username)
        if not pwd_hash :
            return None
        # create object
        return User(username, pwd_hash, True)


    @staticmethod
    def delete(username) :
        """
            Delete user by username
        """
        # get config
        db = shelve.get_shelve('w')
        dic = db['USERS']
        # delete entry
        del dic[username]
        # update config
        db['USERS'] = dic


    @staticmethod 
    def update(username, password) :
        """
            Add or update a user
        """
        # get config
        db = shelve.get_shelve('w')
        dic = db['USERS']
        # create object
        user = User(username, password)
        # create new entry or update value
        dic[username] = user.pw_hash
        # update config
        db['USERS'] = dic


class User(object) :
    """
        User class

        :param name: user name
        :param password: user password
        :param hashed: if the given password is hashed
        :type name: str
        :type password: str
        :type hashed: bool
    """
    def __init__(self, name, password, hashed = False):
        self.name = name
        # hash password if necessary
        if not hashed :
            self.pw_hash = generate_password_hash(password)
        else :
            self.pw_hash = password


    def check_password(self, password) :
        """
            Check password hash

            :param password: clear password to check
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
    

class Links(object) :
    """
        Links API provide static method to deal with static links
    """
    @staticmethod
    def get_all() :
        """
            Get all links from config
        """
        # get all config keys starting with MICROBELINKS_
        db = shelve.get_shelve('r')
        links = {
                key.replace(u'MICROBELINKS_', '') : values
                for key, values in db.iteritems()
                if key.startswith(u'MICROBELINKS_')
                }
        objects = {}
        # create Link object from values
        for key, values in links.iteritems() :
            objects[key] = []
            for tup in values :
                objects[key].append(
                        Link(tup[0], tup[1], tup[2], tup[3])
                )
        return objects


    @staticmethod
    def add(label, url, category) :
        """
            Add a new link

            :param label: link label which is displayed
            :param url: link url
            :param category: link category
        """
        # create a new key from link category
        db = shelve.get_shelve('w')
        key = u'MICROBELINKS_' + category.upper()
        links = db.get(key, [])
        # append a new link
        links.append((
                label,
                url,
                category,
                uuid4().hex
            ))
        # update config
        db[key] = links


    @staticmethod
    def delete(link_id) :
        """
            Delete a link from its id
        """
        # get all config keys starting with MICROBELINKS_
        db = shelve.get_shelve('w')
        links = {
                key : values
                for key, values in db.iteritems()
                if key.startswith(u'MICROBELINKS_')
                }
        # get link with given id
        for key, values in links.iteritems() :
            objects = values
            for value in values :
                if value[3] == link_id :
                    # remove object
                    objects.remove(value)
                    # update config
                    db[key] = objects
                    break

            

class Link(object) :
    """
        Static link class

        :param label: link label
        :param url: link url
        :param category: link category
        :param uid: link id, if not provided will be calculated by uid4()
    """
    def __init__(self, label, url, category, uid = None) :
        if not uid :
            self.uid = uuid4().hex
        else :
            self.uid = uid
        self.label     = label
        self.url       = url
        self.category  = category

    
    @property
    def html(self) :
        """
            Render used by Jinja2 templates
        """
        _template = u'<a href="{}" class="{}" id="{}">{}</a>'
        return _template.format(self.url, self.category, 
                                    self.uid, self.label)


class File(object) :
    """
        Media file object

        :param filename: file name
    """
    def __init__(self, filename) :
        self.name = filename


    @property
    def url(self) :
        """
            File url
        """
        return url_for('static', filename = '/media/' + self.name)


    @property
    def slug(self) :
        """
            File name without ext
        """
        return splitext(self.name)[0]
