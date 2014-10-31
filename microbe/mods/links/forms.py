#! /usr/bin/env python
#-*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    Link forms for Microbe app 
"""

__author__ = 'TROUVERIE Joachim'

from wtforms.validators import Required
from wtforms import TextField

from flask.ext.wtf import Form
from flask.ext.babel import lazy_gettext

from microbe.admin import required_message

class LinkForm(Form) :
    """
        Form to add a new link object
    """
    label = TextField(lazy_gettext(u'Label'), [Required(message=required_message)])
    url = TextField(lazy_gettext(u'Url'), [Required(message=required_message)])
    category = TextField(lazy_gettext(u'Category'), [Required(message=required_message)])