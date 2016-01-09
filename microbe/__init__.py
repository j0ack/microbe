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

    App errors will be logged in

        $HOME/.microbe/microbe.log

    Admin blueprint and extensions are loaded here.
"""

import os
import os.path as op
import logging

from flask import Flask
from flask.ext.themes2 import Themes
from flask.ext.babel import Babel
from logging.handlers import RotatingFileHandler

from microbe.database import db
from microbe.mods.users.models import User

__author__ = 'TROUVERIE Joachim'
__version__ = '1.2.0'


# plugins
babel = Babel()


def _mkdir_if_not_exists(path):
    """Create a new dir if not exists
    :param path: Dir path to create
    """
    if not op.exists(path):
        os.makedirs(path)


def create_app():
    """App factory"""
    # create app
    app = Flask(__name__)
    # config
    app.config.from_pyfile('settings.py')
    # create path if not exists
    path = op.join(op.dirname(__file__), 'content')
    _mkdir_if_not_exists(path)
    _mkdir_if_not_exists(op.join(path, 'pages'))
    _mkdir_if_not_exists(op.join(path, 'posts'))
    _mkdir_if_not_exists(op.join(path, 'comments'))
    # config files
    path = op.join(op.expanduser('~'), '.microbe')
    _mkdir_if_not_exists(path)
    theme_path = op.join(op.dirname(__file__), 'themes')
    if op.lexists(op.join(path, 'themes')):
        os.unlink(op.join(path, 'themes'))
    os.symlink(theme_path, op.join(path, 'themes'))
    # themes support
    Themes(app, app_identifier='microbe')
    # logging
    log_path = op.join(path, 'microbe.log')
    logs = RotatingFileHandler(log_path, 'a', 1024 * 1024, 10)
    frm = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    logs.setFormatter(logging.Formatter(frm))
    app.logger.setLevel(logging.ERROR)
    logs.setLevel(logging.ERROR)
    app.logger.addHandler(logs)
    # plugins
    babel.init_app(app)
    db.init_app(app)
    # frontend
    from microbe.views import frontend, page_not_found
    app.register_blueprint(frontend)
    app.register_error_handler(404, page_not_found)
    # blueprint
    from microbe.admin import admin, lm
    from microbe.mods.email import mail
    app.register_blueprint(admin, url_prefix='/admin')
    lm.init_app(app)
    lm.user_loader(lambda id: User.query.get(id))
    mail.init_app(app)
    return app
