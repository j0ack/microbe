#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    FlatContent forms for Microbe app
"""

from wtforms.validators import Required
from wtforms import TextField, TextAreaField, SelectField

from flask.ext.wtf import Form, RecaptchaField
from flask.ext.babel import lazy_gettext

__author__ = 'TROUVERIE Joachim'

required_message = lazy_gettext('This field is required')


class ContentForm(Form):
    """Form to edit and create new post"""
    title = TextField(lazy_gettext(u'Title'),
                      [Required(message=required_message)])
    content_type = SelectField(lazy_gettext(u'Type'),
                               choices=[(u'posts', u'Post'),
                                        (u'pages', u'Page')])
    category = TextField(lazy_gettext(u'Category'))
    tags = TextField(lazy_gettext(u'Tags'))
    body = TextAreaField(lazy_gettext(u'Content'),
                         validators=[Required(message=required_message)])


class CommentForm(Form):
    """Form to add comment to posts"""
    name = TextField(lazy_gettext(u'Name'),
                     [Required(message=required_message)])
    content = TextAreaField(lazy_gettext(u'Content'),
                            [Required(message=required_message)])
    captcha = RecaptchaField()
