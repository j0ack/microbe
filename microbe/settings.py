#! /usr/bin/env python
# -*- coding : utf-8 -*-


"""
   Default config file for Microbe app
"""

import os.path as op
from uuid import uuid4

__author__ = 'TROUVERIE Joachim'

dirpath = op.dirname(__file__)
key = uuid4().hex


SQLALCHEMY_PATH = op.join(op.expanduser('~'), '.microbe', 'microbe.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + SQLALCHEMY_PATH
SHELVE_FILENAME = op.join(dirpath, 'config.db')
FLATPAGES_ROOT = u'content'
FLATPAGES_EXTENSION = u'.md'
FLATPAGES_AUTO_RELOAD = True
SECRET_KEY = key
WTF_CSRF_SECRET_KEY = key
CSRF_ENABLED = True
DEFAULT_THEME = u'dark'
LANGUAGE = u'en'
PAGINATION = 5
LANGUAGE = u'en'
SITENAME = u'Microbe Default site'
USERS = {u'admin':
         {u'name': u'admin',
          u'email': None,
         u'pw_hash': u'microbe'}}
POST_DIR = u'posts'
PAGE_DIR = u'pages'
SUMMARY_LENGTH = 300
COMMENTS = u'NO'
RSS = u'NO'
