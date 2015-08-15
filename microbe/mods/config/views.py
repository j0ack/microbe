#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Config views for Microbe app
"""

import shelve

from flask import render_template, current_app, url_for, redirect
from flask.ext.login import login_required
from flask.ext.babel import refresh, lazy_gettext

from microbe.admin import admin
from microbe.mods.config.forms import ConfigForm


@admin.route('/config/', methods=['GET', 'POST'])
@login_required
def config():
    """Edit app config from form"""
    # get config
    config = current_app.config
    # populate form with config
    form = ConfigForm(sitename=config.get('SITENAME'),
                      subtitle=config.get('SUBTITLE'),
                      author=config.get('AUTHOR'),
                      language=config.get('LANGUAGE'),
                      pagination=config.get('PAGINATION'),
                      summary_length=config.get('SUMMARY_LENGTH'),
                      comments=config.get('COMMENTS'),
                      rss=config.get('RSS'),
                      recaptcha_public_key=config.get('RECAPTCHA_PUBLIC_KEY'),
                      recaptcha_private_key=config.get('RECAPTCHA_PRIVATE_KEY')
                      )
    if form.validate_on_submit():
        # refresh babel
        path = current_app.config['SHELVE_FILENAME']
        db = shelve.open(path)
        if config.get('LANGUAGE') != db.get('LANGUAGE'):
            refresh()
        db['SITENAME'] = form.sitename.data
        db['SUBTITLE'] = form.subtitle.data
        db['AUTHOR'] = form.author.data
        db['LANGUAGE'] = form.language.data
        db['PAGINATION'] = form.pagination.data
        db['SUMMARY_LENGTH'] = form.summary_length.data
        db['COMMENTS'] = form.comments.data
        db['RSS'] = form.rss.data
        db['RECAPTCHA_PUBLIC_KEY'] = form.recaptcha_public_key.data
        db['RECAPTCHA_PRIVATE_KEY'] = form.recaptcha_private_key.data
        db.close()
        return redirect(url_for('admin.index'))
    return render_template('admin/model.html',
                           form=form,
                           title=lazy_gettext(u'Configuration of ') +
                           config.get('SITENAME'),
                           url=url_for('admin.config'))
