#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Users forms for Microbe app
"""

from wtforms.validators import Required, EqualTo
from wtforms import TextField, PasswordField

from flask.ext.wtf import Form
from flask.ext.babel import lazy_gettext

__author__ = 'TROUVERIE Joachim'

required_message = lazy_gettext('This field is required')


class UserForm(Form):
    """Form to edit and add new user"""
    username = TextField(lazy_gettext(u'Name'),
                         [Required(message=required_message)])
    password = PasswordField(lazy_gettext(u'Password'),
                             [Required(message=required_message),
                              EqualTo('confirm',
                                      message=lazy_gettext(
                                          u'Fields are different'))]
                             )
    confirm = PasswordField(lazy_gettext(u'Confirm'))
