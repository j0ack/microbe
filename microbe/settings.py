#! /usr/bin/env python
#-*- coding : utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
   Default config file for Microbe app 
"""

__author__ = 'TROUVERIE Joachim'


from uuid import uuid4
from os.path import join, dirname

dirpath = dirname(__file__)
key = uuid4().hex

DEBUG=True
CODEMIRROR_LANGUAGES = [u'markdown']
CODEMIRROR_THEME = u'xq-light'
SHELVE_FILENAME = join(dirpath, 'config.db')
PERMANENT_SESSION_LIFETIME = 2678400
FLATPAGES_ROOT = u'content'
FLATPAGES_EXTENSION = u'.md'
FLATPAGES_AUTO_RELOAD = True
SECRET_KEY = key
WTF_CSRF_SECRET_KEY = key
CSRF_ENABLED = True
