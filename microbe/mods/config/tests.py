#! /usr/bin/env python
# -*- coding: utf-8 -*-

from microbe.tests import MicrobeTestCase

__author__ = u'TROUVERIE Joachim'


class ConfigTests(MicrobeTestCase):
    """Tests for config"""
    def setUp(self):
        super(ConfigTests, self).setUp()
        with self.client.session_transaction() as session:
            session['user_id'] = self.user.id

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
