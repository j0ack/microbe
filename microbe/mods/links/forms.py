#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Link forms for Microbe app
"""

from wtforms.validators import Required
from wtforms import TextField

from flask.ext.wtf import Form
from flask.ext.babel import lazy_gettext

__author__ = u'TROUVERIE Joachim'

required_message = lazy_gettext('This field is required')


class LinkForm(Form):
    """Form to add a new link object"""
    label = TextField(lazy_gettext(u'Label'),
                      [Required(message=required_message)])
    url = TextField(lazy_gettext(u'Url'),
                    [Required(message=required_message)])
    category = TextField(lazy_gettext(u'Category'),
                         [Required(message=required_message)])
