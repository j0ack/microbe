#! /usr/bin/env python
# -*- coding: utf-8 -*-

from microbe.tests import MicrobeTestCase
from microbe.mods.links.models import Link, LinkCategory

__author__ = u'TROUVERIE Joachim'


class LinksTests(MicrobeTestCase):
    """Tests for links"""
    def setUp(self):
        super(LinksTests, self).setUp()
        with self.client.session_transaction() as session:
            session['user_id'] = self.user.id

    def test_links(self):
        self.client.post('/admin/link/', data=dict(
            label='test',
            url='http://joacodepel.tk',
            category='Test'
        ))
        # list
        rv = self.client.get('/admin/links/', follow_redirects=True)
        self.assertIn('href="http://joacodepel.tk"', rv.data)
        self.assertIn('class="Test"', rv.data)
        self.assertIn('test</a>', rv.data)
        self.assertEquals(len(Link.query.all()), 1)
        self.assertEquals(len(LinkCategory.query.all()), 1)
        # del
        link = Link.query.first()
        self.client.post('/admin/delete_link/', data=dict(
            link=link.id
        ))
        # list
        self.assertEquals(len(Link.query.all()), 0)
        self.assertEquals(len(LinkCategory.query.all()), 0)
