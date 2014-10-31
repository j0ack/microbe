#! /usr/bin/env python
#-*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    Users forms for Microbe app 
"""

__author__ = 'TROUVERIE Joachim'

from wtforms.validators import Required, EqualTo
from wtforms import TextField, PasswordField

from flask.ext.wtf import Form
from flask.ext.babel import lazy_gettext

from microbe.admin import required_message

class UserForm(Form) :
    """
        Form to edit and add new user
    """
    username = TextField(lazy_gettext(u'Name'), 
                        [Required(message = required_message)])
    password = PasswordField(
                    lazy_gettext(u'Password'), 
                    [
                        Required(message = required_message),
                        EqualTo('confirm', message = lazy_gettext(u'Fields are different'))
                    ]
               )
    confirm  = PasswordField(lazy_gettext(u'Confirm'))