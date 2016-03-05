#! /usr/bin/env python
# -*- coding: utf-8 -*-

import base64
from microbe.tests import MicrobeTestCase

__author__ = u'TROUVERIE Joachim'


class AuthTests(MicrobeTestCase):
    """Tests for auth"""
    def test_login(self):
        rv = self.client.post('/admin/login', data=dict(
            username='test',
            password='test'
        ), follow_redirects=True)
        self.assertIn('Invalid user', rv.data)
        rv = self.client.post('/admin/login', data=dict(
            username='admin_test',
            password='test'
        ), follow_redirects=True)
        self.assertIn('Invalid password', rv.data)
        rv = self.client.post('/admin/login', data=dict(
            username='admin_test',
            password='microbe'
        ), follow_redirects=True)
        with self.client.session_transaction() as sess:
            self.assertEquals(self.user.id, sess['user_id'])

    def test_logout(self):
        self.client.get('/admin/logout', follow_redirects=True)
        with self.client.session_transaction() as sess:
            self.assertNotEquals(self.user.id, sess.get('user_id'))

    def test_basic_auth(self):
        cre = base64.b64encode(b'admin_test:microbe')
        head = {'Authorization': b'Basic ' + cre}
        rv = self.client.get('/admin/', headers=head)
        self.assert200(rv)

    def test_basic_auth_failure(self):
        cre = base64.b64encode(b'admin_test:test')
        head = {'Authorization': b'Basic ' + cre}
        rv = self.client.get('/admin/', headers=head)
        self.assertIn('login', rv.data)

    def test_lost_password(self):
        rv = self.client.post('/admin/lost_password', data=dict(
            username='test',
            email='test@test.com'
        ), follow_redirects=True)
        self.assertIn('Invalid user', rv.data)
        rv = self.client.post('/admin/lost_password', data=dict(
            username='admin_test',
            email='test@test.com'
        ), follow_redirects=True)
        self.assertIn('No email registered for this user', rv.data)
        self.user.email = 'test@test2.com'
        rv = self.client.post('/admin/lost_password', data=dict(
            username='admin_test',
            email='test@test.com'
        ), follow_redirects=True)
        self.assertIn('Invalid email', rv.data)
