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
WHOOSH_BASE = SQLALCHEMY_PATH.replace('microbe.db', 'whoosh')
SECRET_KEY = key
WTF_CSRF_SECRET_KEY = key
CSRF_ENABLED = True
DEFAULT_THEME = u'dark'
LANGUAGE = u'en'
PAGINATION = 5
LANGUAGE = u'en'
SITENAME = u'Microbe Default site'
SUMMARY_LENGTH = 30
COMMENTS = u'NO'
RSS = u'NO'
