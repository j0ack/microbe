#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Auth forms for Microbe app
"""

from wtforms.validators import Required
from wtforms.fields.html5 import EmailField
from wtforms import TextField, PasswordField, BooleanField

from flask.ext.wtf import Form
from flask.ext.babel import lazy_gettext

__author__ = 'TROUVERIE Joachim'

required_message = lazy_gettext('This field is required')


class LoginForm(Form):
    """
        Login form for the admin part
    """
    username = TextField(lazy_gettext(u'User id'),
                         [Required(message=required_message)])
    password = PasswordField(lazy_gettext(u'Password'),
                             [Required(message=required_message)])
    remember = BooleanField(lazy_gettext(u'Remember me'))


class LostPasswordForm(Form):
    """
        Form for lost passwords
    """
    username = TextField(lazy_gettext(u'User name'),
                         [Required(message=required_message)])
    email = EmailField(lazy_gettext(u'User email'),
                       [Required(message=required_message)])
