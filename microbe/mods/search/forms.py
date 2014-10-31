#! /usr/bin/env python
#-*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    Search forms for Microbe app 
"""

__author__ = 'TROUVERIE Joachim'

from wtforms.validators import Required
from wtforms import TextField

from flask.ext.wtf import Form
from flask.ext.babel import lazy_gettext

from microbe.admin import required_message


class SearchForm(Form):
    """
        Form to search in contents
    """
    search = TextField(lazy_gettext(u'Search'), 
            validators = [Required(message=required_message)])
