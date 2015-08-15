#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Config forms for Microbe app
"""

from wtforms.validators import Required
from wtforms import TextField, SelectField, IntegerField

from flask.ext.wtf import Form
from flask.ext.babel import lazy_gettext

__author__ = 'TROUVERIE Joachim'

required_message = lazy_gettext('This field is required')


class ConfigForm(Form):
    """Form to edit config"""
    sitename = TextField(lazy_gettext(u'Site name'),
                         [Required(message=required_message)])
    subtitle = TextField(lazy_gettext(u'Site subtitle (option)'))
    language = SelectField(lazy_gettext(u'Language'),
                           choices=[(u'en', u'English'), (u'fr', u'Francais')])
    author = TextField(lazy_gettext(u'Author (option)'))
    pagination = IntegerField(lazy_gettext(u'Pagination'),
                              [Required(message=required_message)])
    summary_length = IntegerField(lazy_gettext(u'Summary length'),
                                  [Required(message=required_message)])
    comments = SelectField(lazy_gettext(u'Comments'),
                           choices=[(u'YES', lazy_gettext(u'Yes')),
                                    (u'NO', lazy_gettext(u'No'))])
    rss = SelectField(lazy_gettext(u'Atom feed'),
                      choices=[(u'YES', lazy_gettext(u'Yes')),
                               (u'NO', lazy_gettext(u'No'))])
    recaptcha_public_key = TextField(lazy_gettext(u'Recaptcha public key'))
    recaptcha_private_key = TextField(lazy_gettext(u'Recaptcha private key'))

    def validate(self):
        """Override validation

        Check validation between fields
        """
        rv = Form.validate(self)
        if not rv:
            return False
        if self.comments.data == u'YES':
            if not self.recaptcha_public_key.data:
                err = lazy_gettext(u'Mandatory field if comments are enabled')
                self.recaptcha_public_key.errors.append(err)
                return False
            else:
                # check if key is valid
                if len(self.recaptcha_public_key.data) != 40:
                    err = lazy_gettext(u'This key is not valid, check it')
                    self.recaptcha_public_key.errors.append(err)
                    return False
            if not self.recaptcha_private_key.data:
                err = lazy_gettext(u'Mandatory field if comments are enabled')
                self.recaptcha_private_key.errors.append(err)
                return False
            else:
                # check if key is valid
                if len(self.recaptcha_public_key.data) != 40:
                    err = lazy_gettext(u'This key is not valid, check it')
                    self.recaptcha_public_key.errors.append(err)
                    return False
        return True
