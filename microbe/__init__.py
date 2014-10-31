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

import os
import os.path as op

from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.babel import Babel
from flask.ext.themes2 import Themes

from microbe.flatcontent import FlatContent
from microbe.utils import merge_default_config


# create app
app = Flask(__name__)

# config
app.config.from_pyfile('settings.py')

# config
if not op.exists(app.config['SHELVE_FILENAME']) :
    merge_default_config(app.config)

# create path if not exists
path = op.join(op.dirname(__file__), 'content')
if not op.exists(path) :
    os.makedirs(op.join(path, 'pages'))
    os.makedirs(op.join(path, 'posts'))
 
path = op.join(op.expanduser('~'), '.microbe')
theme_path =  op.join(op.dirname(__file__), 'themes')
if not op.exists(path) :
    os.makedirs(path)

if op.exists(op.join(path, 'themes')) :
    os.unlink(op.join(path, 'themes'))

os.symlink(theme_path, op.join(path, 'themes'))

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

# blueprint
from microbe.admin import admin
from microbe.mods.users import load_user
app.register_blueprint(admin, url_prefix = '/admin')
lm.user_loader(load_user)

from microbe import views
