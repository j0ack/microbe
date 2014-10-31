#! /usr/bin/env python
#-*- coding : utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
   Default config file for Microbe app 
"""

__author__ = 'TROUVERIE Joachim'

import os.path as op
from uuid import uuid4

dirpath = op.dirname(__file__)
key = uuid4().hex

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
