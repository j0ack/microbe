#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Users views for Microbe app
"""

from flask import redirect, url_for, request, render_template
from flask.ext.login import login_required
from flask.ext.babel import lazy_gettext

from microbe.admin import admin
from microbe.database import db
from microbe.mods.users.models import User
from microbe.mods.users.forms import UserForm

__author__ = u'TROUVERIE Joachim'


@admin.route('/users/')
@login_required
def users():
    """List users"""
    page = request.args.get('page', 1)
    users = User.query.paginate(page, 15, False)
    return render_template('admin/users.html', objects=users,
                           url=url_for('admin.users'))


@admin.route('/delete-user/', methods=['POST'])
@login_required
def delete_user():
    """Delete a user"""
    user = User.query.get_or_404(request.form['user'])
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.users'))


@admin.route('/user/<user>', methods=['GET', 'POST'])
@admin.route('/user/', methods=['GET', 'POST'])
@login_required
def user(user=None):
    """Edit or create user"""
    # get user
    if user:
        user_obj = User.query.get_or_404(user)
        form = UserForm(username=user_obj.name,
                        email=user_obj.email)
        title = user_obj.name
    else:
        form = UserForm()
        user_obj = None
        title = lazy_gettext(u'New user')
    if form.validate_on_submit():
        # update or add new user
        username = form.username.data
        pwd = form.password.data
        email = form.email.data
        if user_obj:
            user_obj.name = username
            user_obj.set_password(pwd)
            user_obj.email = email
        else:
            user_obj = User(username, pwd, email)
            db.session.add(user_obj)
        db.session.commit()
        return redirect(url_for('.users'))
    return render_template('admin/model.html', title=title,
                           form=form, url=url_for('admin.user', user=user))
