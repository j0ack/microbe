#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from flask.ext.testing import TestCase

from microbe import create_app


class LinksTests(TestCase):
    """Tests for links"""
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        with self.client.session_transaction() as session:
            session['user_id'] = 'admin'

    def test_links(self):
        self.client.post('/admin/link/', data=dict(
            label='test',
            url='http://joacodepel.tk',
            category='Test'
        ))
        # list
        rv = self.client.get('/admin/links/')
        self.assertIn('href="http://joacodepel.tk"', rv.data)
        self.assertIn('class="Test"', rv.data)
        self.assertIn('test</a>', rv.data)
        # del
        uid = self.app.config['MICROBELINKS_TEST'][0][3]
        self.client.post('/admin/delete_link/', data=dict(
            link=uid
        ))
        # list
        rv = self.client.get('/admin/links/')
        self.assertNotIn('href="http://joacodepel.tk"', rv.data)
        self.assertNotIn('class="Test"', rv.data)
        self.assertNotIn('test</a>', rv.data)


if __name__ == '__main__':
    unittest.main()
