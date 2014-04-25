#! /usr/bin/env python
#-*- coding : utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
   Default config file for Microbe app 
"""

__author__ = 'TROUVERIE Joachim'

from werkzeug.security import generate_password_hash
from uuid import uuid4

CODEMIRROR_LANGUAGES = [u'markdown']
CODEMIRROR_THEME = u'xq-light'
PERMANENT_SESSION_LIFETIME = 2678400
LANGUAGE = u'en'
SITENAME = u'Microbe Default site'
USERS = {u'admin' : generate_password_hash(u'microbe')}
FLATPAGES_ROOT = u'content'
POST_DIR = u'posts'
PAGE_DIR = u'pages'
PAGINATION = 5
SUMMARY_LENGTH = 300
FLATPAGES_EXTENSION = u'.md'
FLATPAGES_AUTO_RELOAD = True
COMMENTS = u'NO'
RSS = u'NO'
DEFAULT_THEME = u'dark'
SECRET_KEY = uuid4().hex
