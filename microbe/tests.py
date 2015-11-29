#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.testing import TestCase

from microbe import create_app
from microbe.database import db
from microbe.mods.users.models import User

__author__ = u'TROUVERIE Joachim'


class MicrobeTestCase(TestCase):
    """Tests for Microbe"""
    def create_app(self):
        app = create_app()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.user = User('admin_test', 'microbe', '')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(self.user)
        db.session.commit()
