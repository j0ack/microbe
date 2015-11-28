#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.testing import TestCase

from microbe import create_app
from microbe.database import db
from microbe.mods.users.models import User


class ConfigTests(TestCase):
    """Tests for config"""
    def create_app(self):
        app = create_app()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()
        user = User('admin_test', 'microbe', '')
        db.session.add(user)
        db.session.commit()
        with self.client.session_transaction() as session:
            session['user_id'] = user.id

    def test_config(self):
        rv = self.client.post('/admin/config/', data=dict(
            sitename='',
            subtitle='',
            language='en',
            author='',
            pagination='',
            summary_length='',
            comments='NO',
            rss='NO',
            recaptcha_public_key='',
            recaptcha_private_key=''
        ), follow_redirects=True)
        self.assertIn('This field is required', rv.data)
        rv = self.client.post('/admin/config/', data=dict(
            sitename='Test',
            subtitle='',
            language='en',
            author='',
            pagination=5,
            summary_length=500,
            comments='YES',
            rss='NO',
            recaptcha_public_key='',
            recaptcha_private_key=''
        ), follow_redirects=True)
        self.assertIn('Mandatory field if comments are enabled', rv.data)
        rv = self.client.post('/admin/config/', data=dict(
            sitename='Test',
            subtitle='',
            language='en',
            author='',
            pagination=5,
            summary_length=500,
            comments='YES',
            rss='NO',
            recaptcha_public_key='APAPAPAPAPAPA',
            recaptcha_private_key='APAPAPAPAPAPAP'
        ), follow_redirects=True)
        self.assertIn('This key is not valid, check it', rv.data)
        rv = self.client.post('/admin/config/', data=dict(
            sitename='Test',
            subtitle='',
            language='en',
            author='',
            pagination=5,
            summary_length=500,
            comments='NO',
            rss='NO',
            recaptcha_public_key='',
            recaptcha_private_key=''
        ))
        self.assertRedirects(rv, '/admin/')
