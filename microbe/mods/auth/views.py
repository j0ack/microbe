#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Auth views for Microbe app
"""

from uuid import uuid4

from flask import redirect, url_for, render_template, request, flash
from flask.ext.babel import lazy_gettext
from flask.ext.login import login_user, logout_user, login_required

from microbe.admin import admin
from microbe.database import db
from microbe.mods.auth.forms import LoginForm, LostPasswordForm
from microbe.mods.users.models import User
from microbe.mods.email import send_email

__author__ = 'TROUVERIE Joachim'


@admin.route('/login', methods=['GET', 'POST'])
def login():
    """Login User"""
    # check users and create default user
    if len(User.query.all()) == 0:
        user = User('admin', 'microbe', '')
        db.session.add(user)
        db.session.commit()
    # create form
    form = LoginForm()
    # form submit
    if form.validate_on_submit():
        # check username and password
        user = User.query.filter_by(name=form.username.data).first()
        if not user:
            form.username.errors.append(lazy_gettext(u'Invalid user'))
        elif not user.check_password(form.password.data):
            form.password.errors.append(lazy_gettext(u'Invalid password'))
        else:
            login_user(user, remember=form.remember.data)
            return redirect(request.args.get('next') or url_for('admin.index'))
    return render_template('admin/model.html', form=form, url='')


@admin.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    return redirect(url_for('frontend.index'))


@admin.route('/lost_password', methods=['GET','POST'])
def lost_password():
    """Generate a new password and send it by mail"""
    form = LostPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        email = form.email.data
        if not user:
            form.username.errors.append(lazy_gettext(u'Invalid user'))
        elif user.email != email:
            form.email.errors.append(lazy_gettext(u'Invalid email'))
        elif email:
            password = uuid4().hex
            send_email(lazy_gettext(u'New password'),[email],
                       lazy_gettext(u'Your password has been reset for Microbe, your new password is ' + password))
            user.set_password(password)
            db.session.commit()
            flash(lazy_gettext(u'A new password has been sent to your email address'))
    return render_template('admin/model.html', form=form, ur='')
