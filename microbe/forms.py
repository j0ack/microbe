#! /usr/bin/env python
#-*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    Forms for Microbe app
"""

__author__ = 'TROUVERIE Joachim'


from werkzeug.security import check_password_hash
from wtforms.validators import Required, EqualTo
from wtforms import (TextField, PasswordField, IntegerField, SelectField, 
                    BooleanField, TextAreaField, Field)

from flask.ext.wtf import Form, RecaptchaField
from flask.ext.codemirror.fields import CodeMirrorField
from flask.ext.babel import lazy_gettext


# required message constant
required_message = lazy_gettext(u'This field is required')

class CommentForm(Form) :
    """
        Form to add comment to posts
    """
    name = TextField(lazy_gettext(u'Name'), 
                [Required(message = required_message)])
    content = TextAreaField(lazy_gettext(u'Content'), 
                [Required(message = required_message)])
    captcha = RecaptchaField()


class SearchForm(Form):
    """
        Form to search in contents
    """
    search = TextField(lazy_gettext(u'Search'), 
            validators = [Required()])


class LoginForm(Form) :
    """
        Login form for the admin part
    """
    username = TextField(lazy_gettext(u'User id'), 
                    [Required(message = required_message)])
    password = PasswordField(lazy_gettext(u'Password'), 
                    [Required(message = required_message)])
    remember = BooleanField(lazy_gettext(u'Remember me'))


class ContentForm(Form) :
    """
        Form to edit and create new post
    """
    title        = TextField(lazy_gettext(u'Title'), 
                        [Required(message = required_message)])
    content_type =  SelectField(lazy_gettext(u'Type'), 
                        choices = [(u'posts', u'Post'),(u'pages', u'Page')])
    category     = TextField(lazy_gettext(u'Category'))
    tags         = TextField(lazy_gettext(u'Tags'))
    body         = CodeMirrorField(
                     language='markdown',
                     config = {'lineWrapping' : 'true' },
                     label = lazy_gettext(u'Content'), 
                     validators = [Required(message = required_message)]
                   )


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


class LinkForm(Form) :
    """
        Form to add a new link object
    """
    label = TextField(lazy_gettext(u'Label'), [Required()])
    url = TextField(lazy_gettext(u'Url'), [Required()])
    category = TextField(lazy_gettext(u'Category'), [Required()])


class ConfigForm(Form) :
    """
        Form to edit config
    """
    server_name    = TextField(lazy_gettext(u'Server name'),
                        [Required(message = required_message)])
    sitename       = TextField(lazy_gettext(u'Site name'), 
                        [Required(message = required_message)])
    subtitle       = TextField(lazy_gettext(u'Site subtitle (option)'))
    language       = SelectField(lazy_gettext(u'Language'), 
                        choices = [(u'en', u'English'),(u'fr', u'Français')])
    author         = TextField(lazy_gettext(u'Author (option)'))
    pagination     = IntegerField(lazy_gettext(u'Pagination'), 
                        [Required(message = required_message)])
    summary_length = IntegerField(lazy_gettext(u'Summary length'), 
                        [Required(message = required_message)])
    comments       = SelectField(lazy_gettext(u'Comments'), 
                        choices = [(u'YES', lazy_gettext(u'Yes')),(u'NO', lazy_gettext(u'No'))])
    rss            = SelectField(lazy_gettext(u'Atom feed'), 
                        choices = [(u'YES', lazy_gettext(u'Yes')),(u'NO', lazy_gettext(u'No'))])
    recaptcha_public_key  = TextField(lazy_gettext(u'Recaptcha public key'))
    recaptcha_private_key = TextField(lazy_gettext(u'Recaptcha private key'))

    def validate(self) :
        """
            Override validation

            Check validation between fields
        """
        rv = Form.validate(self)
        if not rv :
            return False
        if self.comments.data == u'YES':
            if not self.recaptcha_public_key.data :
                error = lazy_gettext(u'Mandatory field if comments are enabled')
                self.recaptcha_public_key.errors.append(error)
                return False
            else :
                # check if key is valid
                if len(self.recaptcha_public_key.data) != 40 :
                    error = lazy_gettext(u'This key is not valid, check it')
                    self.recaptcha_public_key.errors.append(error)
                    return False
            if not self.recaptcha_private_key.data :                
                error = lazy_gettext(u'Mandatory field if comments are enabled')
                self.recaptcha_private_key.errors.append(error)
                return False
            else :
                # check if key is valid
                if len(self.recaptcha_public_key.data) != 40 :
                    error = lazy_gettext(u'This key is not valid, check it')
                    self.recaptcha_public_key.errors.append(error)
                    return False
        return True


    def populate_obj(self, out) :
        """
            Override populate obj

            Populate app config from form
        """
        meta = { key.upper() : value.data 
                for key, value in self.__dict__.iteritems()
                if isinstance(value, Field)
                and key != u'crsf_token' 
                and value}
        for key, value in meta.iteritems() :
            out[key] = value
