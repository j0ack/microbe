#! /usr/bin/env python
#-*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    Auth forms for Microbe app 
"""

__author__ = 'TROUVERIE Joachim'

from wtforms.validators import Required
from wtforms import TextField, PasswordField, BooleanField

from flask.ext.wtf import Form
from flask.ext.babel import lazy_gettext


required_message = lazy_gettext('This field is required')


class LoginForm(Form) :
    """
        Login form for the admin part
    """
    username = TextField(lazy_gettext(u'User id'), 
                    [Required(message = required_message)])
    password = PasswordField(lazy_gettext(u'Password'), 
                    [Required(message = required_message)])
    remember = BooleanField(lazy_gettext(u'Remember me'))
