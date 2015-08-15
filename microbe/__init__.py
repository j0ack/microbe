#! /usr/bin/env python
# -*- coding: utf-8 -*-


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

import os
import os.path as op

from flask import Flask
from flask.ext.themes2 import Themes
from flask.ext.babel import Babel

from microbe.utils import merge_default_config
from microbe.flatcontent import FlatContent

__author__ = 'TROUVERIE Joachim'
__version__ = '1.2.0'


# plugins
contents = FlatContent()
babel = Babel()


def create_app():
    """App factory"""
    # create app
    app = Flask(__name__)
    # config
    app.config.from_pyfile('settings.py')
    # config
    if not op.exists(app.config['SHELVE_FILENAME']):
        merge_default_config(app.config)
    # create path if not exists
    path = op.join(op.dirname(__file__), 'content')
    if not op.exists(path):
        os.makedirs(op.join(path, 'pages'))
        os.makedirs(op.join(path, 'posts'))
    path = op.join(op.expanduser('~'), '.microbe')
    theme_path = op.join(op.dirname(__file__), 'themes')
    if not op.exists(path):
        os.makedirs(path)
    if op.exists(op.join(path, 'themes')):
        os.unlink(op.join(path, 'themes'))
    os.symlink(theme_path, op.join(path, 'themes'))
    # themes support
    Themes(app, app_identifier='microbe')
    # plugins
    contents.init_app(app)
    babel.init_app(app)
    # frontend
    from microbe.views import frontend, page_not_found
    app.register_blueprint(frontend)
    app.register_error_handler(404, page_not_found)
    # blueprint
    from microbe.admin import admin, lm
    from microbe.mods.users import load_user
    app.register_blueprint(admin, url_prefix='/admin')
    lm.init_app(app)
    lm.user_loader(load_user)
    return app
