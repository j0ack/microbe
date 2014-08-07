#! /usr/bin/env python
#-*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    Microbe app
    -----------

    Create Microbe app

    Settings will be loaded from settings.py if available,
    else default settings will be loaded from default_settings.py.

    If it is the first time the application is launched a 
    symbolic link will be created in $HOME dir to themes dir :

        $HOME/.microbe/themes

    Admin blueprint and extensions are loaded here.
"""

__author__ = 'TROUVERIE Joachim'

import os.path as op
from os import makedirs, symlink

from flatcontent import FlatContent
from utils import merge_default_config

from flask import Flask
from flask.ext.codemirror import CodeMirror
from flask.ext.login import LoginManager
from flask.ext.babel import Babel
from flask.ext.themes2 import Themes

# create app
app = Flask(__name__)

# config
path = op.join(op.dirname(__file__), 'settings.py')
app.config.from_pyfile('settings.py')

# config
merge_default_config(app.config)

# create path if not exists
path =  op.join(op.dirname(__file__), 'content')
if not op.exists(path) :
    makedirs(op.join(path, 'pages'))
    makedirs(op.join(path, 'posts'))
 
path = op.join(op.expanduser('~'), '.microbe')
theme_path =  op.join(op.dirname(__file__), 'themes')
if not op.exists(path) :
    makedirs(path)
    symlink(theme_path, op.join(path, 'themes'))

# flatpages
contents = FlatContent(app)

# login
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'admin.login'

# translations
babel = Babel(app)

# themes support
Themes(app, app_identifier = 'microbe')

# codemirror
codemirror = CodeMirror(app)

# blueprint
from admin import bp as admin_module
from admin import load_user
app.register_blueprint(admin_module, url_prefix = '/admin')
lm.user_loader(load_user)

from flask_debugtoolbar import DebugToolbarExtension
toolbar = DebugToolbarExtension(app)

from microbe import views
