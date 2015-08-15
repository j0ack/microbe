#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Search forms for Microbe app
"""

from wtforms.validators import Required
from wtforms import TextField

from flask.ext.wtf import Form
from flask.ext.babel import lazy_gettext

__author__ = 'TROUVERIE Joachim'

required_message = lazy_gettext('This field is required')


class SearchForm(Form):
    """Form to search in contents"""
    search = TextField(lazy_gettext(u'Search'),
                       validators=[Required(message=required_message)])
