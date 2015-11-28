#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.testing import TestCase

from microbe import create_app
from microbe.database import db
from microbe.mods.users.models import User
from microbe.mods.links.models import Link, LinkCategory


class LinksTests(TestCase):
    """Tests for links"""
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
