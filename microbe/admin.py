#! /usr/bin/env python
#-*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    Admin BluePrint for Microbe app 
"""

__author__ = 'TROUVERIE Joachim'

from flask import Blueprint, render_template
from flask.ext.babel import lazy_gettext
from flask.ext.login import login_required

# create blueprint
admin = Blueprint('admin', __name__)

# required message contant
required_message = lazy_gettext('This field is required')

@admin.route('/')
@login_required
def index() :
    """
        Admin index view
    """
    return render_template('admin/index.html')

from microbe.mods.auth import views
from microbe.mods.comments import views
from microbe.mods.config import views
from microbe.mods.contents import views
from microbe.mods.links import views
from microbe.mods.themes import views
from microbe.mods.users import views
from microbe.mods.media import views
