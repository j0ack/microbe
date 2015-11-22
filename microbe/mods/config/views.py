#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Config views for Microbe app
"""

from flask import render_template, current_app, url_for, redirect
from flask.ext.login import login_required
from flask.ext.babel import refresh, lazy_gettext

from microbe.database import db
from microbe.admin import admin
from microbe.mods.config.forms import ConfigForm
from microbe.mods.config.models import Config

__author__ = u'TROUVERIE Joachim'


@admin.route('/config/', methods=['GET', 'POST'])
@login_required
def config():
    """Edit app config from form"""
    # get config
    config = Config.query.first() or Config()
    # populate form with config
    form = ConfigForm(config)
    if form.validate_on_submit():
        form.populate_obj(config)
        # refresh babel
        if current_app.config.get('LANGUAGE') != config.language:
            refresh()
        if not Config.query.first():
            db.session.add(config)
        db.session.commit()
        return redirect(url_for('admin.index'))
    return render_template('admin/model.html',
                           form=form,
                           title=lazy_gettext(u'Configuration of ') +
                           config.sitename,
                           url=url_for('admin.config'))
