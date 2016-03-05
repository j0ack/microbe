#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Themes views for Microbe app
"""

from flask import (current_app, render_template, url_for, redirect, request,
                   abort)

from flask.ext.themes2 import get_themes_list

from microbe.admin import admin
from microbe.database import db
from microbe.mods.auth.decorator import auth_required
from microbe.mods.config.models import Config


@admin.route('/themes/')
@auth_required
def themes():
    """List available themes"""
    current_app.theme_manager.refresh()
    themes = get_themes_list()
    default_theme = current_app.config['DEFAULT_THEME']
    selected = current_app.config.get(u'THEME', default_theme)
    return render_template('admin/themes.html', themes=themes,
                           selected=selected)


@admin.route('/set-theme/', methods=['POST'])
@auth_required
def set_theme():
    """Set theme in config to be displayed to users"""
    ident = request.form.get('theme')
    config = Config.query.first() or Config()
    if ident not in current_app.theme_manager.themes:
        abort(404)
    config.theme = ident
    if not Config.query.first():
        db.session.add(config)
    db.session.commit()
    return redirect(url_for('admin.themes'))
