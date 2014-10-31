#! /usr/bin/env python
#-*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    Themes views for Microbe app 
"""

import shelve

from flask import current_app, render_template, url_for, redirect, request, abort
from flask.ext.themes2 import get_themes_list
from flask.ext.login import login_required

from microbe.admin import admin

@admin.route('/themes/')
@login_required
def themes() :
    """
        List available themes
    """
    current_app.theme_manager.refresh()
    themes = get_themes_list()
    default_theme = current_app.config['DEFAULT_THEME']
    selected = current_app.config.get(u'THEME', default_theme)
    return render_template('admin/themes.html', themes = themes, 
            selected = selected)


@admin.route('/set-theme/', methods=['POST'])
@login_required
def set_theme():
    """
        Set theme in config to be displayed to users
    """
    ident = request.form.get('theme')
    path = current_app.config['SHELVE_FILENAME']    
    db = shelve.open(path)
    if ident not in current_app.theme_manager.themes :
        abort(404)
    db['THEME'] = ident
    db.close()
    return redirect(url_for('admin.themes'))
