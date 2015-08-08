#! /usr/bin/env python
#-*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    Auth views for Microbe app 
"""

__author__ = 'TROUVERIE Joachim'


from flask import redirect, url_for, render_template, request
from flask.ext.babel import lazy_gettext
from flask.ext.login import login_user, logout_user, login_required

from microbe.admin import admin
from microbe.mods.auth.forms import LoginForm
from microbe.mods.users.models import Users

@admin.route('/login', methods=['GET','POST'])
def login() :
    """
        Login User
    """
    # create form
    form = LoginForm()
    # form submit
    if form.validate_on_submit() :
        # check username and password
        user = Users.get(form.username.data)
        if not user :
            form.username.errors.append(lazy_gettext(u'Invalid user'))
        elif not user.check_password(form.password.data) :
            form.password.errors.append(lazy_gettext(u'Invalid password'))
        else :
            login_user(user, remember = form.remember.data)
            return redirect(request.args.get('next') or url_for('admin.index'))
    return render_template('admin/model.html', form = form, url = '')


@admin.route('/logout')
@login_required
def logout() :
    """
        Logout user
    """
    logout_user()
    return redirect(url_for('frontend.index'))
