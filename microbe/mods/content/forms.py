#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    FlatContent forms for Microbe app
"""

from wtforms.validators import Required
from wtforms.fields.html5 import EmailField
from wtforms import TextField, TextAreaField, SelectField, BooleanField

from flask.ext.wtf import Form, RecaptchaField
from flask.ext.babel import lazy_gettext

__author__ = u'TROUVERIE Joachim'

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
    body = TextAreaField(lazy_gettext(u'Content'))

    def __init__(self, obj=None):
        super(ContentForm, self).__init__(obj=obj)
        if obj:
            self.category.data = obj.category.label
            self.tags.data = ','.join([tag.label for tag in obj.tags])


class CommentForm(Form):
    """Form to add comment to posts"""
    name = TextField(lazy_gettext(u'Name'),
                     [Required(message=required_message)])
    email = EmailField(lazy_gettext(u'Email'))
    site = TextField(lazy_gettext(u'Site'))
    content = TextAreaField(lazy_gettext(u'Content'),
                            [Required(message=required_message)])
    notify = BooleanField(
        lazy_gettext(u'Notify me of follow-up comments by email'))
    captcha = RecaptchaField()

    def validate(self):
        """Override validate
        Check consistency between fields
        """
        test = Form.validate(self)
        if not test:
            return test
        # check if email is not empty if ask for notification
        if self.notify.data:
            if not self.email.data:
                txt = u'This field is required if you want to be notified'
                self.email.errors.append(txt)
                return False
        return True
