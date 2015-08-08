#! /usr/bin/env python
#-*- coding: utf-8 -*-


"""
    Admin BluePrint for Microbe app 
"""

__author__ = 'TROUVERIE Joachim'


import urllib2
import json

from microbe import __version__

from flask import Blueprint, render_template
from flask.ext.babel import lazy_gettext
from flask.ext.login import LoginManager, login_required


# create blueprint
admin = Blueprint('admin', __name__)
lm = LoginManager()
lm.login_view = 'admin.login'


@admin.route('/')
@login_required
def index() :
    """
        Admin index view
    """
    html = urllib2.urlopen('https://pypi.python.org/pypi/microbe/json/')
    json_data = html.read()
    data = json.loads(json_data)
    info = data.get('info')
    if info:
        version = info.get('version')
    new_version = version and version != __version__
    return render_template('admin/index.html', new_version = new_version)

from microbe.mods.auth import views
from microbe.mods.comments import views
from microbe.mods.config import views
from microbe.mods.contents import views
from microbe.mods.links import views
from microbe.mods.themes import views
from microbe.mods.users import views
from microbe.mods.media import views
