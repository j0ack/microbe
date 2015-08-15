#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Users views for Microbe app
"""

from flask import current_app, redirect, url_for, request, render_template
from flask.ext.login import login_required
from flask.ext.babel import lazy_gettext

from microbe.admin import admin
from microbe.utils import render_list
from microbe.mods.users.models import Users
from microbe.mods.users.forms import UserForm

__author__ = 'TROUVERIE Joachim'


@admin.route('/users/')
@login_required
def users():
    """List users"""
    users = current_app.config['USERS']
    lst = users.keys()
    return render_list('admin/users.html', lst, per_page=15)


@admin.route('/delete-user/', methods=['POST'])
@login_required
def delete_user():
    """Delete a user"""
    user = request.form['user']
    Users.delete(user)
    return redirect(url_for('admin.users'))


@admin.route('/user/<user>', methods=['GET', 'POST'])
@admin.route('/user/', methods=['GET', 'POST'])
@login_required
def user(user=None):
    """Edit or create user"""
    # get user
    if user:
        form = UserForm(username=user)
        title = user
    else:
        form = UserForm()
        title = lazy_gettext(u'New user')
    if form.validate_on_submit():
        # update or add new user
        username = form.username.data
        pwd = form.password.data
        Users.update(username, pwd)
        return redirect(url_for('.users'))
    return render_template('admin/model.html', title=title,
                           form=form, url=url_for('admin.user'))
