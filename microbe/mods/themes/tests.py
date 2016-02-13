#! /usr/bin/env python
# -*- coding: utf-8 -*-

from microbe.tests import MicrobeTestCase

__author__ = u'TROUVERIE Joachim'


class ThemeTests(MicrobeTestCase):
    """Tests for themes management"""
    def setUp(self):
        super(ThemeTests, self).setUp()
        with self.client.session_transaction() as session:
            session['user_id'] = self.user.id

    def test_themes(self):
        rv = self.client.post('/admin/set-theme/', data=dict(
            theme='not-used-id'
        ), follow_redirects=True)
        self.assert404(rv)
        rv = self.client.post('/admin/set-theme/', data=dict(
            theme='dark'
        ), follow_redirects=False)
        self.assertRedirects(rv, '/admin/themes/')
